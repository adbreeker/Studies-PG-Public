import React, { useState, useEffect, useCallback } from 'react';
import { HubConnectionBuilder } from '@microsoft/signalr';
import styles from '../styles/analytics.module.css';

function AnalyticsPageSimple() {
  const [departurePreferences, setDeparturePreferences] = useState([]);
  const [realTimeData, setRealTimeData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    period: 'monthly',
    dateFrom: '',
    dateTo: ''
  });

  const ANALYTICS_SERVICE_URL = import.meta.env.VITE_ANALYTICS_SERVICE_URL || '/api/analytics';  // Format API data to match frontend expectations
  const formatApiData = useCallback((apiData) => {
    console.log('?? Formatting API data:', apiData);
    
    if (!Array.isArray(apiData)) {
      console.warn('?? API data is not an array:', apiData);
      return [];
    }

    return apiData.map((item, index) => {
      console.log(`?? Processing item ${index}:`, item);
        // Generate realistic mock price based on route and reservations (deterministic)
      const generateMockPrice = (departure, arrival, reservations) => {
        const basePrice = 500; // Base price in PLN
        const popularityMultiplier = Math.max(1, reservations / 50); // Higher price for popular routes
        
        // Create a deterministic "random" factor based on route name
        const routeString = `${departure}-${arrival}`;
        let hash = 0;
        for (let i = 0; i < routeString.length; i++) {
          const char = routeString.charCodeAt(i);
          hash = ((hash << 5) - hash) + char;
          hash = hash & hash; // Convert to 32-bit integer
        }
        
        // Convert hash to a number between 0.5 and 2.5
        const routeDistance = Math.abs(hash % 200) / 100 + 0.5; // Range: 0.5-2.5
        
        return Math.round((basePrice * routeDistance * popularityMultiplier) * 100) / 100;
      };
      
      // Map backend field names to frontend expected names
      const formatted = {
        id: index + 1,
        departureDirection: `${item.DepartureStation || item.departureStation || 'Unknown'} -> ${item.ArrivalStation || item.arrivalStation || 'Unknown'}`,
        totalReservations: item.ReservationCount || item.reservationCount || 0,
        averagePrice: generateMockPrice(
          item.DepartureStation || item.departureStation,
          item.ArrivalStation || item.arrivalStation,
          item.ReservationCount || item.reservationCount || 0
        ),
        // Use actual period dates from backend - DO NOT override with calculated dates
        periodStart: item.PeriodStart || item.periodStart || item.DepartureDate || item.departureDate,
        periodEnd: item.PeriodEnd || item.periodEnd || item.DepartureDate || item.departureDate,
        percentage: item.Percentage || item.percentage || 0,
        mostPopularRoute: item.MostPopularRoute || item.mostPopularRoute
      };
      
      console.log(`? Formatted item ${index}:`, formatted);
      return formatted;
    });
  }, []);const fetchDeparturePreferences = useCallback(async () => {
    console.log('?? Fetching departure preferences with filters:', filters);
    try {
      const queryParams = new URLSearchParams();
      if (filters.period) queryParams.append('period', filters.period);
      if (filters.dateFrom) queryParams.append('startDate', filters.dateFrom);
      if (filters.dateTo) queryParams.append('endDate', filters.dateTo);

      const url = `${ANALYTICS_SERVICE_URL}/departure-direction-preferences?${queryParams}`;
      console.log('?? API URL:', url);

      const response = await fetch(url);
      console.log('?? Response status:', response.status, response.statusText);
      
      if (!response.ok) throw new Error('Failed to fetch departure preferences');
      
      const data = await response.json();
      console.log('?? Raw departure preferences data:', data);
      
      if (Array.isArray(data) && data.length > 0) {
        console.log('?? First item structure:', data[0]);
      }
      
      // Format the data to match frontend expectations
      const formattedData = formatApiData(data);
      setDeparturePreferences(formattedData);
    } catch (err) {
      console.error('? Error fetching departure preferences:', err);
      console.error('? Error stack:', err.stack);
      setError('Failed to load departure preferences');
    } finally {
      setLoading(false);
    }
  }, [ANALYTICS_SERVICE_URL, filters, formatApiData]);

  const fetchRealTimeAnalytics = useCallback(async () => {
    console.log('?? Fetching real-time analytics...');
    try {
      const url = `${ANALYTICS_SERVICE_URL}/real-time`;
      console.log('?? Real-time API URL:', url);

      const response = await fetch(url);
      console.log('?? Real-time response status:', response.status, response.statusText);
      
      if (!response.ok) throw new Error('Failed to fetch real-time analytics');
      
      const data = await response.json();
      console.log('?? Raw real-time data:', data);
      
      if (data && data.lastUpdated) {
        console.log('?? LastUpdated field:', {
          value: data.lastUpdated,
          type: typeof data.lastUpdated,
          dateConversion: new Date(data.lastUpdated),
          isValidDate: !isNaN(new Date(data.lastUpdated))
        });
      }
      
      setRealTimeData(data);
    } catch (err) {
      console.error('? Error fetching real-time analytics:', err);
      console.error('? Error stack:', err.stack);
    }
  }, [ANALYTICS_SERVICE_URL]);
  // Effect for SignalR connection setup
  useEffect(() => {    console.log('Starting SignalR connection setup...');
    console.log('?? SignalR URL will be: http://localhost:5223/analyticsHub');
    
    let newConnection = null;
    let mounted = true;

    const setupConnection = async () => {
      try {        // Establish SignalR connection
        // Connect directly to analytics service instead of through proxy
        const hubUrl = 'http://localhost:5223/analyticsHub';
        console.log('?? Connecting directly to SignalR hub at:', hubUrl);
        
        newConnection = new HubConnectionBuilder()
          .withUrl(hubUrl, {
            withCredentials: false,
            transport: 1 | 2 // WebSockets | ServerSentEvents fallback
          })
          .withAutomaticReconnect()
          .build();if (mounted) {
          // No need to set connection state as we're tracking with isConnected
        }// Add connection state event handlers
        newConnection.onclose((error) => {
          console.log('SignalR connection closed:', error);
          if (mounted) {
            setIsConnected(false);
          }
        });

        newConnection.onreconnecting((error) => {
          console.log('SignalR connection reconnecting...', error);
          if (mounted) {
            setIsConnected(false);
          }
        });

        newConnection.onreconnected(() => {
          console.log('SignalR connection reconnected');
          if (mounted) {
            setIsConnected(true);
          }
        });        // Set up event handlers before starting
        newConnection.on('AnalyticsUpdated', (data) => {
          console.log('?? Received AnalyticsUpdated:', data);
          if (mounted && data) {
            // Validate that data has expected structure
            if (data && typeof data === 'object') {
              setRealTimeData(data);
            } else {
              console.warn('?? Received invalid AnalyticsUpdated data:', data);
            }
          }
        });

        newConnection.on('DeparturePreferencesUpdated', (data) => {
          console.log('?? Received DeparturePreferencesUpdated:', data);
          if (mounted && data) {
            // Validate that data is an array before formatting
            if (Array.isArray(data) && data.length > 0) {
              const formattedData = formatApiData(data);
              setDeparturePreferences(formattedData);
            } else {
              console.warn('?? Received invalid DeparturePreferencesUpdated data:', data);
            }
          }
        });// Start the connection
        if (mounted) {
          await newConnection.start();
          console.log('? Connected to analytics hub successfully');
          setIsConnected(true);
        }
      } catch (err) {
        console.error('? Error connecting to analytics hub:', err);
        console.error('? Connection state:', newConnection?.state);
        if (mounted) {
          setError('Failed to connect to real-time analytics: ' + err.message);
        }
      }
    };

    setupConnection();    return () => {
      mounted = false;
      if (newConnection) {
        console.log('?? Stopping SignalR connection...');
        newConnection.stop().catch(err => console.error('Error stopping connection:', err));
      }
    };  }, [formatApiData, ANALYTICS_SERVICE_URL, filters]); // Include filters as dependency

  // Effect for initial data loading
  useEffect(() => {
    console.log('?? Component mounted or dependencies changed');
    console.log('?? Current filters:', filters);
    console.log('?? ANALYTICS_SERVICE_URL:', ANALYTICS_SERVICE_URL);
    
    fetchDeparturePreferences();
    fetchRealTimeAnalytics();
  }, [fetchDeparturePreferences, fetchRealTimeAnalytics, ANALYTICS_SERVICE_URL, filters]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };
  const applyFilters = () => {
    setLoading(true);
    fetchDeparturePreferences();
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Loading analytics data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>{error}</div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Train Reservation Analytics</h1>
      <p className={styles.subtitle}>Real-time insights into customer departure direction preferences</p>

      {/* Real-time Stats */}
      {realTimeData && (
        <div className={styles.realTimeSection}>
          <h2>Real-time Statistics</h2>
          <div className={styles.statsGrid}>            <div className={styles.statCard}>
              <h3>Total Reservations</h3>
              <div className={styles.statValue}>{realTimeData.totalReservations}</div>
            </div>
            <div className={styles.statCard}>
              <h3>Last Updated</h3>
              <div className={styles.statValue}>
                {(() => {
                  console.log('?? Rendering lastUpdated:', {
                    raw: realTimeData.lastUpdated,
                    type: typeof realTimeData.lastUpdated,
                    dateObj: new Date(realTimeData.lastUpdated),
                    isValid: !isNaN(new Date(realTimeData.lastUpdated))
                  });
                  
                  const date = new Date(realTimeData.lastUpdated);
                  return isNaN(date) ? 'Invalid Date' : date.toLocaleTimeString();
                })()}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className={styles.filtersSection}>
        <h2>Filters</h2>
        <div className={styles.filters}>
          <div className={styles.filterGroup}>
            <label htmlFor="period">Period:</label>
            <select
              id="period"
              name="period"
              value={filters.period}
              onChange={handleFilterChange}
            >
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
          <div className={styles.filterGroup}>
            <label htmlFor="dateFrom">From:</label>
            <input
              type="date"
              id="dateFrom"
              name="dateFrom"
              value={filters.dateFrom}
              onChange={handleFilterChange}
            />
          </div>
          <div className={styles.filterGroup}>
            <label htmlFor="dateTo">To:</label>
            <input
              type="date"
              id="dateTo"
              name="dateTo"
              value={filters.dateTo}
              onChange={handleFilterChange}
            />
          </div>
          <button className={styles.applyButton} onClick={applyFilters}>
            Apply Filters
          </button>
        </div>
      </div>

      {/* Departure Direction Preferences */}
      <div className={styles.preferencesSection}>
        <h2>Departure Direction Preferences</h2>
        {departurePreferences.length === 0 ? (
          <div className={styles.noData}>No data available for the selected period</div>
        ) : (
          <div className={styles.preferencesGrid}>            {departurePreferences.map((pref, index) => (
              <div key={index} className={styles.preferenceCard}>
                <div className={styles.directionHeader}>
                  <h3>{pref.departureDirection || 'Unknown Direction'}</h3>
                </div>
                <div className={styles.preferenceStats}>
                  <div className={styles.statItem}>
                    <span className={styles.statLabel}>Reservations:</span>
                    <span className={styles.statValue}>{pref.totalReservations}</span>
                  </div>                  <div className={styles.statItem}>
                    <span className={styles.statLabel}>Avg Price:</span>
                    <span className={styles.statValue}>
                      {typeof pref.averagePrice === 'number' ? `PLN ${pref.averagePrice.toFixed(2)}` : 'N/A'}
                    </span>
                  </div><div className={styles.statItem}>
                    <span className={styles.statLabel}>Period:</span>
                    <span className={styles.statValue}>
                      {(() => {
                        console.log('?? Rendering period dates for item:', {
                          periodStart: pref.periodStart,
                          periodStartType: typeof pref.periodStart,
                          periodEnd: pref.periodEnd,
                          periodEndType: typeof pref.periodEnd,
                          periodStartDate: new Date(pref.periodStart),
                          periodEndDate: new Date(pref.periodEnd),
                          periodStartValid: !isNaN(new Date(pref.periodStart)),
                          periodEndValid: !isNaN(new Date(pref.periodEnd))
                        });
                        
                        const startDate = new Date(pref.periodStart);
                        const endDate = new Date(pref.periodEnd);
                        const startStr = isNaN(startDate) ? 'Invalid Date' : startDate.toLocaleDateString();
                        const endStr = isNaN(endDate) ? 'Invalid Date' : endDate.toLocaleDateString();
                        
                        return `${startStr} - ${endStr}`;
                      })()}
                    </span>
                  </div>
                  {pref.mostPopularRoute && (
                    <div className={styles.statItem}>
                      <span className={styles.statLabel}>Popular Route:</span>
                      <span className={styles.statValue}>{pref.mostPopularRoute}</span>
                    </div>
                  )}
                </div>
                <div className={styles.progressBar}>
                  <div 
                    className={styles.progressFill} 
                    style={{ 
                      width: `${Math.min(100, (pref.totalReservations / Math.max(...departurePreferences.map(p => p.totalReservations))) * 100)}%` 
                    }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>      {/* Connection Status */}
      <div className={styles.connectionStatus}>
        <span className={isConnected ? styles.connected : styles.disconnected}>
          {isConnected ? 'Real-time connected' : 'Real-time disconnected'}
        </span>
      </div>
    </div>
  );
}

export default AnalyticsPageSimple;
