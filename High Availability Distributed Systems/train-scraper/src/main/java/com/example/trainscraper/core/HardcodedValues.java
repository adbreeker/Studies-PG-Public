package com.example.trainscraper.core;

import org.springframework.core.style.DefaultToStringStyler;

public class HardcodedValues {
    public static final String GD_GW = """
            {
                "scrapingId": "e3235d44-cad0-4f05-8a4e-0972fb48b60e",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 1,
                        "departureScheduled": "17:36",
                        "departureReal": null,
                        "arrivalScheduled": "17:39",
                        "arrivalReal": null,
                        "travelTime": "03 min",
                        "price": "15,00 zł",
                        "trainId": "45104",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 2,
                        "departureScheduled": "17:43",
                        "departureReal": null,
                        "arrivalScheduled": "17:47",
                        "arrivalReal": null,
                        "travelTime": "04 min",
                        "price": "5,50 zł",
                        "trainId": "55413",
                        "routeSections": [],
                        "carriers": [
                            "PR"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 3,
                        "departureScheduled": "18:28",
                        "departureReal": null,
                        "arrivalScheduled": "18:32",
                        "arrivalReal": null,
                        "travelTime": "04'",
                        "price": "5,50",
                        "trainId": "50475",
                        "routeSections": [],
                        "carriers": [
                            "R"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 4,
                        "departureScheduled": "18:49",
                        "departureReal": null,
                        "arrivalScheduled": "18:53",
                        "arrivalReal": null,
                        "travelTime": "0h 4min",
                        "price": "15,00 PLN",
                        "trainId": "45102",
                        "routeSections": [
                            {
                                "id": 1,
                                "sectionName": "Gdańsk Gł. -> Gdańsk Wrzeszcz",
                                "classAvailabilities": [
                                    {
                                        "id": 1,
                                        "className": "Class 1",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 2,
                                        "className": "Class 2",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "TLK"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 5,
                        "departureScheduled": "18:09",
                        "departureReal": null,
                        "arrivalScheduled": "18:15",
                        "arrivalReal": null,
                        "travelTime": "06'",
                        "price": "",
                        "trainId": "95793",
                        "routeSections": [],
                        "carriers": [
                            "SKM-T",
                            "SKM"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 6,
                        "departureScheduled": "18:21",
                        "departureReal": null,
                        "arrivalScheduled": "18:25",
                        "arrivalReal": null,
                        "travelTime": "04'",
                        "price": "5,50",
                        "trainId": "50641",
                        "routeSections": [],
                        "carriers": [
                            "R"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 7,
                        "departureScheduled": "18:29",
                        "departureReal": null,
                        "arrivalScheduled": "18:35",
                        "arrivalReal": null,
                        "travelTime": "06'",
                        "price": "5,50",
                        "trainId": "95795",
                        "routeSections": [],
                        "carriers": [
                            "SKM"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 8,
                        "departureScheduled": "18:07",
                        "departureReal": null,
                        "arrivalScheduled": "18:11",
                        "arrivalReal": null,
                        "travelTime": "04'",
                        "price": "",
                        "trainId": "38108",
                        "routeSections": [],
                        "carriers": [
                            "TLK"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 9,
                        "departureScheduled": "18:13",
                        "departureReal": null,
                        "arrivalScheduled": "18:17",
                        "arrivalReal": null,
                        "travelTime": "04'",
                        "price": "48,00",
                        "trainId": "4505",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 10,
                        "departureScheduled": "17:49",
                        "departureReal": null,
                        "arrivalScheduled": "17:55",
                        "arrivalReal": null,
                        "travelTime": "06 min",
                        "price": "5,50 zł",
                        "trainId": "95681",
                        "routeSections": [],
                        "carriers": [
                            "SKM-T"
                        ],
                        "delayed": false
                    }
                ],
                "reason": null
            }""";
     public static String GG_WC = """
            {
                "scrapingId": "4fbcc2db-1794-4e46-81a8-0b8a0d0c717b",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 11,
                        "departureScheduled": "00:04",
                        "departureReal": null,
                        "arrivalScheduled": "03:45",
                        "arrivalReal": null,
                        "travelTime": "03h41'",
                        "price": "71,00",
                        "trainId": "83170",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 12,
                        "departureScheduled": "17:57",
                        "departureReal": null,
                        "arrivalScheduled": "21:00",
                        "arrivalReal": null,
                        "travelTime": "3h03",
                        "price": "71,00 zł",
                        "trainId": "51100",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 13,
                        "departureScheduled": "19:46",
                        "departureReal": null,
                        "arrivalScheduled": "22:30",
                        "arrivalReal": null,
                        "travelTime": "2h 44min",
                        "price": "169,00 PLN",
                        "trainId": "5100",
                        "routeSections": [
                            {
                                "id": 2,
                                "sectionName": "Gdańsk Gł. -> Warszawa Centr.",
                                "classAvailabilities": [
                                    {
                                        "id": 3,
                                        "className": "Class 1",
                                        "availability": "No information on seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 4,
                                        "className": "Class 2",
                                        "availability": "No information on seat availability",
                                        "specialSeatInfo": "no information"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 14,
                        "departureScheduled": "20:00",
                        "departureReal": null,
                        "arrivalScheduled": "23:00",
                        "arrivalReal": null,
                        "travelTime": "3h",
                        "price": "71,00 PLN",
                        "trainId": "5188",
                        "routeSections": [
                            {
                                "id": 3,
                                "sectionName": "Gdańsk Gł. -> Warszawa Centr.",
                                "classAvailabilities": [
                                    {
                                        "id": 5,
                                        "className": "Class 1",
                                        "availability": "Last available seats",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 6,
                                        "className": "Class 2",
                                        "availability": "Last available seats",
                                        "specialSeatInfo": "no information"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 15,
                        "departureScheduled": "17:51",
                        "departureReal": null,
                        "arrivalScheduled": "20:30",
                        "arrivalReal": null,
                        "travelTime": "2h39",
                        "price": "169,00 zł",
                        "trainId": "5310",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 16,
                        "departureScheduled": "18:46",
                        "departureReal": null,
                        "arrivalScheduled": "21:30",
                        "arrivalReal": null,
                        "travelTime": "02h44'",
                        "price": "169,00",
                        "trainId": "5102",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 17,
                        "departureScheduled": "20:21",
                        "departureReal": null,
                        "arrivalScheduled": "23:35",
                        "arrivalReal": null,
                        "travelTime": "03h14'",
                        "price": "71,00",
                        "trainId": "53170",
                        "routeSections": [],
                        "carriers": [
                            "TLK"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 18,
                        "departureScheduled": "21:28",
                        "departureReal": null,
                        "arrivalScheduled": "01:05",
                        "arrivalReal": null,
                        "travelTime": "03h37'",
                        "price": "71,00",
                        "trainId": "81150",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";
     public static String GG_KG = """
            {
                "scrapingId": "b39eabd0-bbbb-46db-abe5-a13303524d11",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 19,
                        "departureScheduled": "18:46",
                        "departureReal": null,
                        "arrivalScheduled": "00:39",
                        "arrivalReal": null,
                        "travelTime": "05h53'",
                        "price": "185,00",
                        "trainId": "5102, 5320",
                        "routeSections": [],
                        "carriers": [
                            "EIP",
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 20,
                        "departureScheduled": "00:04",
                        "departureReal": null,
                        "arrivalScheduled": "07:55",
                        "arrivalReal": null,
                        "travelTime": "07h51'",
                        "price": "89,00",
                        "trainId": "83170",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 21,
                        "departureScheduled": "17:51",
                        "departureReal": null,
                        "arrivalScheduled": "23:03",
                        "arrivalReal": null,
                        "travelTime": "5h12",
                        "price": "225,00 zł",
                        "trainId": "5310",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 22,
                        "departureScheduled": "05:52",
                        "departureReal": null,
                        "arrivalScheduled": "11:56",
                        "arrivalReal": null,
                        "travelTime": "06h04'",
                        "price": "87,00",
                        "trainId": "53104",
                        "routeSections": [],
                        "carriers": [
                            "TLK"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 23,
                        "departureScheduled": "05:46",
                        "departureReal": null,
                        "arrivalScheduled": "11:04",
                        "arrivalReal": null,
                        "travelTime": "05h18'",
                        "price": "225,00",
                        "trainId": "5300",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 24,
                        "departureScheduled": "20:21",
                        "departureReal": null,
                        "arrivalScheduled": "03:40",
                        "arrivalReal": null,
                        "travelTime": "07h19'",
                        "price": "93,00",
                        "trainId": "53170",
                        "routeSections": [],
                        "carriers": [
                            "TLK"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 25,
                        "departureScheduled": "23:40",
                        "departureReal": null,
                        "arrivalScheduled": "08:47",
                        "arrivalReal": null,
                        "travelTime": "09h07'",
                        "price": "94,00",
                        "trainId": "461",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";
     public static String GG_PG = """
    {
    "scrapingId": "0bf0a6c2-69f8-4a71-930b-21e345b40800",
    "status": "COMPLETED",
    "results": [
        {
            "id": 26,
            "departureScheduled": "04:56",
            "departureReal": null,
            "arrivalScheduled": "08:18",
            "arrivalReal": null,
            "travelTime": "03h22'",
            "price": "70,00",
            "trainId": "57108",
            "routeSections": [],
            "carriers": [
                "IC"
            ],
            "delayed": true
        },
        {
            "id": 27,
            "departureScheduled": "06:14",
            "departureReal": null,
            "arrivalScheduled": "09:19",
            "arrivalReal": null,
            "travelTime": "03h05'",
            "price": "70,00",
            "trainId": "56100",
            "routeSections": [],
            "carriers": [
                "IC"
            ],
            "delayed": true
        },
        {
            "id": 28,
            "departureScheduled": "18:21",
            "departureReal": null,
            "arrivalScheduled": "21:22",
            "arrivalReal": null,
            "travelTime": "03h01'",
            "price": "70,00",
            "trainId": "5600",
            "routeSections": [],
            "carriers": [
                "IC"
            ],
            "delayed": true
        },
        {
            "id": 29,
            "departureScheduled": "19:16",
            "departureReal": null,
            "arrivalScheduled": "22:17",
            "arrivalReal": null,
            "travelTime": "03h01'",
            "price": "70,00",
            "trainId": "5700",
            "routeSections": [],
            "carriers": [
                "IC"
            ],
            "delayed": true
        },
        {
            "id": 30,
            "departureScheduled": "04:29",
            "departureReal": null,
            "arrivalScheduled": "07:20",
            "arrivalReal": null,
            "travelTime": "02h51'",
            "price": "70,00",
            "trainId": "261",
            "routeSections": [],
            "carriers": [
                "IC"
            ],
            "delayed": true
        },
        {
            "id": 31,
            "departureScheduled": "23:40",
            "departureReal": null,
            "arrivalScheduled": "02:42",
            "arrivalReal": null,
            "travelTime": "03h02'",
            "price": "70,00",
            "trainId": "461",
            "routeSections": [],
            "carriers": [
                "IC"
            ],
            "delayed": true
        }
    ],
    "reason": null
}

""";

     public static String GG_GW = """
            {
                "scrapingId": "5db8dae2-1144-409e-8a3f-8b61a49f8047",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 32,
                        "departureScheduled": "18:24",
                        "departureReal": null,
                        "arrivalScheduled": "18:28",
                        "arrivalReal": null,
                        "travelTime": "04'",
                        "price": "5,50",
                        "trainId": "50618",
                        "routeSections": [],
                        "carriers": [
                            "R"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 33,
                        "departureScheduled": "19:39",
                        "departureReal": null,
                        "arrivalScheduled": "19:43",
                        "arrivalReal": null,
                        "travelTime": "0h 4min",
                        "price": "48,00 PLN",
                        "trainId": "5100",
                        "routeSections": [
                            {
                                "id": 4,
                                "sectionName": "Gdańsk Wrzeszcz -> Gdańsk Gł.",
                                "classAvailabilities": [
                                    {
                                        "id": 7,
                                        "className": "Class 1",
                                        "availability": "High seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 8,
                                        "className": "Class 2",
                                        "availability": "High seat availability",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 34,
                        "departureScheduled": "17:44",
                        "departureReal": null,
                        "arrivalScheduled": "17:48",
                        "arrivalReal": null,
                        "travelTime": "04 min",
                        "price": "48,00 zł",
                        "trainId": "5310",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 35,
                        "departureScheduled": "18:39",
                        "departureReal": null,
                        "arrivalScheduled": "18:43",
                        "arrivalReal": null,
                        "travelTime": "04'",
                        "price": "48,00",
                        "trainId": "5102",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 36,
                        "departureScheduled": "18:35",
                        "departureReal": null,
                        "arrivalScheduled": "18:42",
                        "arrivalReal": null,
                        "travelTime": "07'",
                        "price": "5,50",
                        "trainId": "59784",
                        "routeSections": [],
                        "carriers": [
                            "SKM"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 37,
                        "departureScheduled": "17:55",
                        "departureReal": null,
                        "arrivalScheduled": "18:02",
                        "arrivalReal": null,
                        "travelTime": "07 min",
                        "price": "5,50 zł",
                        "trainId": "59780",
                        "routeSections": [],
                        "carriers": [
                            "SKM-T"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 38,
                        "departureScheduled": "18:02",
                        "departureReal": null,
                        "arrivalScheduled": "18:06",
                        "arrivalReal": null,
                        "travelTime": "04 min",
                        "price": "5,50 zł",
                        "trainId": "55272",
                        "routeSections": [],
                        "carriers": [
                            "PR"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 39,
                        "departureScheduled": "17:50",
                        "departureReal": null,
                        "arrivalScheduled": "17:54",
                        "arrivalReal": null,
                        "travelTime": "04 min",
                        "price": "15,00 zł",
                        "trainId": "51100",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 40,
                        "departureScheduled": "18:55",
                        "departureReal": null,
                        "arrivalScheduled": "19:02",
                        "arrivalReal": null,
                        "travelTime": "07'",
                        "price": "5,50",
                        "trainId": "59786",
                        "routeSections": [],
                        "carriers": [
                            "SKM"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 41,
                        "departureScheduled": "18:56",
                        "departureReal": null,
                        "arrivalScheduled": "19:00",
                        "arrivalReal": null,
                        "travelTime": "04'",
                        "price": "5,50",
                        "trainId": "55436",
                        "routeSections": [],
                        "carriers": [
                            "R"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 42,
                        "departureScheduled": "17:56",
                        "departureReal": null,
                        "arrivalScheduled": "18:01",
                        "arrivalReal": null,
                        "travelTime": "05 min",
                        "price": "15,00 zł",
                        "trainId": "85104",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 43,
                        "departureScheduled": "17:35",
                        "departureReal": null,
                        "arrivalScheduled": "17:42",
                        "arrivalReal": null,
                        "travelTime": "07 min",
                        "price": "5,50 zł",
                        "trainId": "59688",
                        "routeSections": [],
                        "carriers": [
                            "SKM-T"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 44,
                        "departureScheduled": "19:10",
                        "departureReal": null,
                        "arrivalScheduled": "19:14",
                        "arrivalReal": null,
                        "travelTime": "04'",
                        "price": "15,00",
                        "trainId": "5700",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";
     public static String GW_GG = """
             {
                 "scrapingId": "67372771-5092-4ae0-ab8a-71a7f0ac1d23",
                 "status": "COMPLETED",
                 "results": [
                     {
                         "id": 1,
                         "departureScheduled": "18:55",
                         "departureReal": null,
                         "arrivalScheduled": "19:02",
                         "arrivalReal": null,
                         "travelTime": "07 min",
                         "price": "5,50 zł",
                         "trainId": "59786",
                         "routeSections": [],
                         "carriers": [
                             "SKM-T"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 2,
                         "departureScheduled": "18:56",
                         "departureReal": null,
                         "arrivalScheduled": "19:00",
                         "arrivalReal": null,
                         "travelTime": "04 min",
                         "price": "5,50 zł",
                         "trainId": "55436",
                         "routeSections": [],
                         "carriers": [
                             "PR"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 3,
                         "departureScheduled": "19:39",
                         "departureReal": null,
                         "arrivalScheduled": "19:43",
                         "arrivalReal": null,
                         "travelTime": "0h 4min",
                         "price": "48,00 PLN",
                         "trainId": "5100",
                         "routeSections": [
                             {
                                 "id": 1,
                                 "sectionName": "Gdańsk Wrzeszcz -> Gdańsk Gł.",
                                 "classAvailabilities": [
                                     {
                                         "id": 1,
                                         "className": "Class 1",
                                         "availability": "High seat availability",
                                         "specialSeatInfo": "no information"
                                     },
                                     {
                                         "id": 2,
                                         "className": "Class 2",
                                         "availability": "High seat availability",
                                         "specialSeatInfo": "A special seat is available"
                                     }
                                 ]
                             }
                         ],
                         "carriers": [
                             "EIP"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 4,
                         "departureScheduled": "19:53",
                         "departureReal": null,
                         "arrivalScheduled": "19:57",
                         "arrivalReal": null,
                         "travelTime": "0h 4min",
                         "price": "15,00 PLN",
                         "trainId": "5188",
                         "routeSections": [
                             {
                                 "id": 2,
                                 "sectionName": "Gdańsk Wrzeszcz -> Gdańsk Gł.",
                                 "classAvailabilities": [
                                     {
                                         "id": 3,
                                         "className": "Class 1",
                                         "availability": "Limited seat availability",
                                         "specialSeatInfo": "no information"
                                     },
                                     {
                                         "id": 4,
                                         "className": "Class 2",
                                         "availability": "Limited seat availability",
                                         "specialSeatInfo": "no information"
                                     }
                                 ]
                             }
                         ],
                         "carriers": [
                             "IC"
                         ],
                         "delayed": true
                     },
                     {
                         "id": 5,
                         "departureScheduled": "18:39",
                         "departureReal": null,
                         "arrivalScheduled": "18:43",
                         "arrivalReal": null,
                         "travelTime": "04 min",
                         "price": "48,00 zł",
                         "trainId": "5102",
                         "routeSections": [],
                         "carriers": [
                             "EIP"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 6,
                         "departureScheduled": "19:18",
                         "departureReal": null,
                         "arrivalScheduled": "19:25",
                         "arrivalReal": null,
                         "travelTime": "07'",
                         "price": "5,50",
                         "trainId": "59788",
                         "routeSections": [],
                         "carriers": [
                             "SKM-T",
                             "SKM"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 7,
                         "departureScheduled": "19:55",
                         "departureReal": null,
                         "arrivalScheduled": "20:02",
                         "arrivalReal": null,
                         "travelTime": "07'",
                         "price": "5,50",
                         "trainId": "59792",
                         "routeSections": [],
                         "carriers": [
                             "SKM"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 8,
                         "departureScheduled": "18:35",
                         "departureReal": null,
                         "arrivalScheduled": "18:42",
                         "arrivalReal": null,
                         "travelTime": "07 min",
                         "price": "5,50 zł",
                         "trainId": "59784",
                         "routeSections": [],
                         "carriers": [
                             "SKM-T"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 9,
                         "departureScheduled": "19:10",
                         "departureReal": null,
                         "arrivalScheduled": "19:14",
                         "arrivalReal": null,
                         "travelTime": "04'",
                         "price": "",
                         "trainId": "5700",
                         "routeSections": [],
                         "carriers": [
                             "IC"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 10,
                         "departureScheduled": "19:35",
                         "departureReal": null,
                         "arrivalScheduled": "19:42",
                         "arrivalReal": null,
                         "travelTime": "07'",
                         "price": "5,50",
                         "trainId": "59790",
                         "routeSections": [],
                         "carriers": [
                             "SKM"
                         ],
                         "delayed": false
                     }
                 ],
                 "reason": null
             }""";
     public static String GW_WC = """
            {
                "scrapingId": "201207a4-e5e1-4376-a94d-ccc3c88d65b1",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 45,
                        "departureScheduled": "23:55",
                        "departureReal": null,
                        "arrivalScheduled": "03:45",
                        "arrivalReal": null,
                        "travelTime": "03h50'",
                        "price": "71,00",
                        "trainId": "83170",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 46,
                        "departureScheduled": "17:50",
                        "departureReal": null,
                        "arrivalScheduled": "21:00",
                        "arrivalReal": null,
                        "travelTime": "3h10",
                        "price": "71,00 zł",
                        "trainId": "51100",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 47,
                        "departureScheduled": "19:39",
                        "departureReal": null,
                        "arrivalScheduled": "22:30",
                        "arrivalReal": null,
                        "travelTime": "2h 51min",
                        "price": "169,00 PLN",
                        "trainId": "5100",
                        "routeSections": [
                            {
                                "id": 5,
                                "sectionName": "Gdańsk Wrzeszcz -> Warszawa Centr.",
                                "classAvailabilities": [
                                    {
                                        "id": 9,
                                        "className": "Class 1",
                                        "availability": "High seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 10,
                                        "className": "Class 2",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 48,
                        "departureScheduled": "19:53",
                        "departureReal": null,
                        "arrivalScheduled": "23:00",
                        "arrivalReal": null,
                        "travelTime": "3h 7min",
                        "price": "71,00 PLN",
                        "trainId": "5188",
                        "routeSections": [
                            {
                                "id": 6,
                                "sectionName": "Gdańsk Wrzeszcz -> Warszawa Centr.",
                                "classAvailabilities": [
                                    {
                                        "id": 11,
                                        "className": "Class 1",
                                        "availability": "Last available seats",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 12,
                                        "className": "Class 2",
                                        "availability": "Brak wolnych miejsc",
                                        "specialSeatInfo": "no information"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 49,
                        "departureScheduled": "17:44",
                        "departureReal": null,
                        "arrivalScheduled": "20:30",
                        "arrivalReal": null,
                        "travelTime": "2h46",
                        "price": "169,00 zł",
                        "trainId": "5310",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 50,
                        "departureScheduled": "18:39",
                        "departureReal": null,
                        "arrivalScheduled": "21:30",
                        "arrivalReal": null,
                        "travelTime": "02h51'",
                        "price": "169,00",
                        "trainId": "5102",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 51,
                        "departureScheduled": "20:14",
                        "departureReal": null,
                        "arrivalScheduled": "23:35",
                        "arrivalReal": null,
                        "travelTime": "03h21'",
                        "price": "71,00",
                        "trainId": "53170",
                        "routeSections": [],
                        "carriers": [
                            "TLK"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 52,
                        "departureScheduled": "21:20",
                        "departureReal": null,
                        "arrivalScheduled": "01:05",
                        "arrivalReal": null,
                        "travelTime": "03h45'",
                        "price": "71,00",
                        "trainId": "81150",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            } """;
     public static String GW_KG= """
            {
                "scrapingId": "18cf569d-224a-461a-be51-22bc5af182a1",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 53,
                        "departureScheduled": "18:39",
                        "departureReal": null,
                        "arrivalScheduled": "00:39",
                        "arrivalReal": null,
                        "travelTime": "06h00'",
                        "price": "186,00",
                        "trainId": "5102, 5320",
                        "routeSections": [],
                        "carriers": [
                            "EIP",
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 54,
                        "departureScheduled": "23:55",
                        "departureReal": null,
                        "arrivalScheduled": "07:55",
                        "arrivalReal": null,
                        "travelTime": "08h00'",
                        "price": "89,00",
                        "trainId": "83170",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 55,
                        "departureScheduled": "05:45",
                        "departureReal": null,
                        "arrivalScheduled": "11:56",
                        "arrivalReal": null,
                        "travelTime": "06h11'",
                        "price": "88,00",
                        "trainId": "53104",
                        "routeSections": [],
                        "carriers": [
                            "TLK"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 56,
                        "departureScheduled": "05:39",
                        "departureReal": null,
                        "arrivalScheduled": "11:04",
                        "arrivalReal": null,
                        "travelTime": "05h25'",
                        "price": "225,00",
                        "trainId": "5300",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 57,
                        "departureScheduled": "20:14",
                        "departureReal": null,
                        "arrivalScheduled": "03:40",
                        "arrivalReal": null,
                        "travelTime": "07h26'",
                        "price": "93,00",
                        "trainId": "53170",
                        "routeSections": [],
                        "carriers": [
                            "TLK"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 58,
                        "departureScheduled": "23:33",
                        "departureReal": null,
                        "arrivalScheduled": "08:47",
                        "arrivalReal": null,
                        "travelTime": "09h14'",
                        "price": "95,00",
                        "trainId": "461",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";
     public static String GW_PG = """
            {
                "scrapingId": "98681aa6-e67a-4495-87f3-10f7561273e9",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 59,
                        "departureScheduled": "04:49",
                        "departureReal": null,
                        "arrivalScheduled": "08:18",
                        "arrivalReal": null,
                        "travelTime": "03h29'",
                        "price": "70,00",
                        "trainId": "57108",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 60,
                        "departureScheduled": "06:06",
                        "departureReal": null,
                        "arrivalScheduled": "09:19",
                        "arrivalReal": null,
                        "travelTime": "03h13'",
                        "price": "70,00",
                        "trainId": "56100",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 61,
                        "departureScheduled": "18:12",
                        "departureReal": null,
                        "arrivalScheduled": "21:22",
                        "arrivalReal": null,
                        "travelTime": "3h10",
                        "price": "70,00 zł",
                        "trainId": "5600",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 62,
                        "departureScheduled": "19:10",
                        "departureReal": null,
                        "arrivalScheduled": "22:17",
                        "arrivalReal": null,
                        "travelTime": "3h 7min",
                        "price": "70,00 PLN",
                        "trainId": "5700",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 63,
                        "departureScheduled": "19:39",
                        "departureReal": null,
                        "arrivalScheduled": "02:03",
                        "arrivalReal": null,
                        "travelTime": "6h24",
                        "price": "238,00 zł",
                        "trainId": "5100, 18170",
                        "routeSections": [],
                        "carriers": [
                            "EIP",
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 64,
                        "departureScheduled": "04:21",
                        "departureReal": null,
                        "arrivalScheduled": "07:20",
                        "arrivalReal": null,
                        "travelTime": "02h59'",
                        "price": "70,00",
                        "trainId": "261",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 65,
                        "departureScheduled": "23:33",
                        "departureReal": null,
                        "arrivalScheduled": "02:42",
                        "arrivalReal": null,
                        "travelTime": "3h 9min",
                        "price": "70,00 PLN",
                        "trainId": "461",
                        "routeSections": [
                            {
                                "id": 7,
                                "sectionName": "Gdańsk Wrzeszcz -> Poznań Gł.",
                                "classAvailabilities": [
                                    {
                                        "id": 13,
                                        "className": "Class 1",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 14,
                                        "className": "Class 2",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 66,
                        "departureScheduled": "07:26",
                        "departureReal": null,
                        "arrivalScheduled": "10:20",
                        "arrivalReal": null,
                        "travelTime": "02h54'",
                        "price": "70,00",
                        "trainId": "230",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";
     public static String WC_GG = """
             {
                 "scrapingId": "5b088beb-5244-44f5-a961-21016ba7c536",
                 "status": "COMPLETED",
                 "results": [
                     {
                         "id": 1,
                         "departureScheduled": "21:00",
                         "departureReal": null,
                         "arrivalScheduled": "04:53",
                         "arrivalReal": null,
                         "travelTime": "7h 53min",
                         "price": "68,95 PLN",
                         "trainId": "1530, 460",
                         "routeSections": [
                             {
                                 "id": 1,
                                 "sectionName": "Warszawa Centr. -> Bydgoszcz Gł.",
                                 "classAvailabilities": [
                                     {
                                         "id": 1,
                                         "className": "Class 1",
                                         "availability": "High seat availability",
                                         "specialSeatInfo": "no information"
                                     },
                                     {
                                         "id": 2,
                                         "className": "Class 2",
                                         "availability": "Last available seats",
                                         "specialSeatInfo": "A special seat is available"
                                     }
                                 ]
                             },
                             {
                                 "id": 2,
                                 "sectionName": "Bydgoszcz Gł. -> Gdańsk Gł.",
                                 "classAvailabilities": [
                                     {
                                         "id": 3,
                                         "className": "Class 1",
                                         "availability": "Limited seat availability",
                                         "specialSeatInfo": "no information"
                                     },
                                     {
                                         "id": 4,
                                         "className": "Class 2",
                                         "availability": "Limited seat availability",
                                         "specialSeatInfo": "A special seat is available"
                                     }
                                 ]
                             }
                         ],
                         "carriers": [
                             "IC",
                             "IC"
                         ],
                         "delayed": true
                     },
                     {
                         "id": 2,
                         "departureScheduled": "18:30",
                         "departureReal": null,
                         "arrivalScheduled": "21:06",
                         "arrivalReal": null,
                         "travelTime": "2h36",
                         "price": "169,00 zł",
                         "trainId": "3502",
                         "routeSections": [],
                         "carriers": [
                             "EIP"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 3,
                         "departureScheduled": "05:00",
                         "departureReal": null,
                         "arrivalScheduled": "08:28",
                         "arrivalReal": null,
                         "travelTime": "03h28'",
                         "price": "71,00",
                         "trainId": "1588",
                         "routeSections": [],
                         "carriers": [
                             "IC"
                         ],
                         "delayed": true
                     },
                     {
                         "id": 4,
                         "departureScheduled": "19:00",
                         "departureReal": null,
                         "arrivalScheduled": "22:06",
                         "arrivalReal": null,
                         "travelTime": "3h06",
                         "price": "71,00 zł",
                         "trainId": "35104",
                         "routeSections": [],
                         "carriers": [
                             "TLK"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 5,
                         "departureScheduled": "19:30",
                         "departureReal": null,
                         "arrivalScheduled": "22:12",
                         "arrivalReal": null,
                         "travelTime": "02h42'",
                         "price": "169,00",
                         "trainId": "3500",
                         "routeSections": [],
                         "carriers": [
                             "EIP"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 6,
                         "departureScheduled": "20:30",
                         "departureReal": null,
                         "arrivalScheduled": "23:12",
                         "arrivalReal": null,
                         "travelTime": "2h 42min",
                         "price": "169,00 PLN",
                         "trainId": "4500",
                         "routeSections": [
                             {
                                 "id": 3,
                                 "sectionName": "Warszawa Centr. -> Gdańsk Gł.",
                                 "classAvailabilities": [
                                     {
                                         "id": 5,
                                         "className": "Class 1",
                                         "availability": "High seat availability",
                                         "specialSeatInfo": "no information"
                                     },
                                     {
                                         "id": 6,
                                         "className": "Class 2",
                                         "availability": "Last available seats",
                                         "specialSeatInfo": "A special seat is available"
                                     }
                                 ]
                             }
                         ],
                         "carriers": [
                             "EIP"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 7,
                         "departureScheduled": "02:20",
                         "departureReal": null,
                         "arrivalScheduled": "06:01",
                         "arrivalReal": null,
                         "travelTime": "03h41'",
                         "price": "71,00",
                         "trainId": "38170",
                         "routeSections": [],
                         "carriers": [
                             "IC"
                         ],
                         "delayed": true
                     },
                     {
                         "id": 8,
                         "departureScheduled": "04:30",
                         "departureReal": null,
                         "arrivalScheduled": "07:58",
                         "arrivalReal": null,
                         "travelTime": "03h28'",
                         "price": "71,00",
                         "trainId": "35170",
                         "routeSections": [],
                         "carriers": [
                             "TLK"
                         ],
                         "delayed": true
                     }
                 ],
                 "reason": null
             }""";
     public static String WC_KG = """
             {
                 "scrapingId": "08748660-b108-4b02-8e21-e02d8b979403",
                 "status": "COMPLETED",
                 "results": [
                     {
                         "id": 1,
                         "departureScheduled": "20:10",
                         "departureReal": null,
                         "arrivalScheduled": "23:57",
                         "arrivalReal": null,
                         "travelTime": "3h47",
                         "price": "70,00 zł",
                         "trainId": "143",
                         "routeSections": [],
                         "carriers": [
                             "IC"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 2,
                         "departureScheduled": "18:40",
                         "departureReal": null,
                         "arrivalScheduled": "21:04",
                         "arrivalReal": null,
                         "travelTime": "2h24",
                         "price": "169,00 zł",
                         "trainId": "1312",
                         "routeSections": [],
                         "carriers": [
                             "EIP"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 3,
                         "departureScheduled": "22:04",
                         "departureReal": null,
                         "arrivalScheduled": "00:39",
                         "arrivalReal": null,
                         "travelTime": "2h35",
                         "price": "68,00 zł",
                         "trainId": "5320",
                         "routeSections": [],
                         "carriers": [
                             "IC"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 4,
                         "departureScheduled": "20:40",
                         "departureReal": null,
                         "arrivalScheduled": "23:03",
                         "arrivalReal": null,
                         "travelTime": "2h23",
                         "price": "169,00 zł",
                         "trainId": "5310",
                         "routeSections": [],
                         "carriers": [
                             "EIP"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 5,
                         "departureScheduled": "20:00",
                         "departureReal": null,
                         "arrivalScheduled": "22:40",
                         "arrivalReal": null,
                         "travelTime": "2h40",
                         "price": "68,00 zł",
                         "trainId": "407",
                         "routeSections": [],
                         "carriers": [
                             "IC"
                         ],
                         "delayed": false
                     },
                     {
                         "id": 6,
                         "departureScheduled": "23:48",
                         "departureReal": null,
                         "arrivalScheduled": "03:40",
                         "arrivalReal": null,
                         "travelTime": "3h52",
                         "price": "73,00 zł",
                         "trainId": "53170",
                         "routeSections": [],
                         "carriers": [
                             "TLK"
                         ],
                         "delayed": false
                     }
                 ],
                 "reason": null
             }""" ;
     public static String WC_GW = """
            {
                "scrapingId": "09883ef8-a05a-4417-a2b6-8eca94f79ca2",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 67,
                        "departureScheduled": "21:00",
                        "departureReal": null,
                        "arrivalScheduled": "04:53",
                        "arrivalReal": null,
                        "travelTime": "07h53'",
                        "price": "68,95",
                        "trainId": "1530, 460",
                        "routeSections": [],
                        "carriers": [
                            "IC",
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 68,
                        "departureScheduled": "18:30",
                        "departureReal": null,
                        "arrivalScheduled": "21:06",
                        "arrivalReal": null,
                        "travelTime": "02h36'",
                        "price": "169,00",
                        "trainId": "3502",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 69,
                        "departureScheduled": "19:00",
                        "departureReal": null,
                        "arrivalScheduled": "22:06",
                        "arrivalReal": null,
                        "travelTime": "3h 6min",
                        "price": "71,00 PLN",
                        "trainId": "35104",
                        "routeSections": [
                            {
                                "id": 8,
                                "sectionName": "Warszawa Centr. -> Gdańsk Gł.",
                                "classAvailabilities": [
                                    {
                                        "id": 15,
                                        "className": "Class 1",
                                        "availability": "No information on seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 16,
                                        "className": "Class 2",
                                        "availability": "No information on seat availability",
                                        "specialSeatInfo": "no information"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "TLK"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 70,
                        "departureScheduled": "19:30",
                        "departureReal": null,
                        "arrivalScheduled": "22:12",
                        "arrivalReal": null,
                        "travelTime": "2h 42min",
                        "price": "169,00 PLN",
                        "trainId": "3500",
                        "routeSections": [
                            {
                                "id": 9,
                                "sectionName": "Warszawa Centr. -> Gdańsk Gł.",
                                "classAvailabilities": [
                                    {
                                        "id": 17,
                                        "className": "Class 1",
                                        "availability": "No information on seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 18,
                                        "className": "Class 2",
                                        "availability": "No information on seat availability",
                                        "specialSeatInfo": "no information"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 71,
                        "departureScheduled": "20:30",
                        "departureReal": null,
                        "arrivalScheduled": "23:12",
                        "arrivalReal": null,
                        "travelTime": "02h42'",
                        "price": "169,00",
                        "trainId": "4500",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 72,
                        "departureScheduled": "17:30",
                        "departureReal": null,
                        "arrivalScheduled": "20:12",
                        "arrivalReal": null,
                        "travelTime": "2h42",
                        "price": "169,00 zł",
                        "trainId": "4502",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 73,
                        "departureScheduled": "02:20",
                        "departureReal": null,
                        "arrivalScheduled": "06:01",
                        "arrivalReal": null,
                        "travelTime": "03h41'",
                        "price": "71,00",
                        "trainId": "38170",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";

     public static String WC_KK = """
            {
                "scrapingId": "673b0181-45ba-4b22-a333-7be08a32ea78",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 1,
                        "departureScheduled": "20:10",
                        "departureReal": null,
                        "arrivalScheduled": "23:57",
                        "arrivalReal": null,
                        "travelTime": "3h47",
                        "price": "70,00 zł",
                        "trainId": "143",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 2,
                        "departureScheduled": "18:40",
                        "departureReal": null,
                        "arrivalScheduled": "21:04",
                        "arrivalReal": null,
                        "travelTime": "2h24",
                        "price": "169,00 zł",
                        "trainId": "1312",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 3,
                        "departureScheduled": "18:10",
                        "departureReal": null,
                        "arrivalScheduled": "21:55",
                        "arrivalReal": null,
                        "travelTime": "3h45",
                        "price": "70,00 zł",
                        "trainId": "1322",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 4,
                        "departureScheduled": "20:40",
                        "departureReal": null,
                        "arrivalScheduled": "23:03",
                        "arrivalReal": null,
                        "travelTime": "2h23",
                        "price": "169,00 zł",
                        "trainId": "5310",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 5,
                        "departureScheduled": "20:00",
                        "departureReal": null,
                        "arrivalScheduled": "22:40",
                        "arrivalReal": null,
                        "travelTime": "2h40",
                        "price": "68,00 zł",
                        "trainId": "407",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 6,
                        "departureScheduled": "17:40",
                        "departureReal": null,
                        "arrivalScheduled": "20:03",
                        "arrivalReal": null,
                        "travelTime": "2h23",
                        "price": "169,00 zł",
                        "trainId": "5308",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    }
                ],
                "reason": null
            } """;
     public static String WC_PG = """
            {
                "scrapingId": "0f99120b-075e-4026-bd1e-8cf0aed85038",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 7,
                        "departureScheduled": "19:30",
                        "departureReal": null,
                        "arrivalScheduled": "22:13",
                        "arrivalReal": null,
                        "travelTime": "02h43'",
                        "price": "",
                        "trainId": "27100",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 8,
                        "departureScheduled": "05:00",
                        "departureReal": null,
                        "arrivalScheduled": "07:24",
                        "arrivalReal": null,
                        "travelTime": "02h24'",
                        "price": "149,00",
                        "trainId": "248",
                        "routeSections": [],
                        "carriers": [
                            "EIC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 9,
                        "departureScheduled": "17:30",
                        "departureReal": null,
                        "arrivalScheduled": "20:13",
                        "arrivalReal": null,
                        "travelTime": "2h43",
                        "price": "69,00 zł",
                        "trainId": "17100",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 10,
                        "departureScheduled": "23:34",
                        "departureReal": null,
                        "arrivalScheduled": "04:45",
                        "arrivalReal": null,
                        "travelTime": "05h11'",
                        "price": "95,70",
                        "trainId": "16170, 78813",
                        "routeSections": [],
                        "carriers": [
                            "IC",
                            "KW"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 11,
                        "departureScheduled": "05:30",
                        "departureReal": null,
                        "arrivalScheduled": "08:23",
                        "arrivalReal": null,
                        "travelTime": "02h53'",
                        "price": "69,00",
                        "trainId": "1806",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 12,
                        "departureScheduled": "05:04",
                        "departureReal": null,
                        "arrivalScheduled": "10:44",
                        "arrivalReal": null,
                        "travelTime": "05h40'",
                        "price": "60,00",
                        "trainId": "17502",
                        "routeSections": [],
                        "carriers": [
                            "IR"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 13,
                        "departureScheduled": "18:00",
                        "departureReal": null,
                        "arrivalScheduled": "20:19",
                        "arrivalReal": null,
                        "travelTime": "2h19",
                        "price": "149,00 zł",
                        "trainId": "1802",
                        "routeSections": [],
                        "carriers": [
                            "EIC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 14,
                        "departureScheduled": "22:50",
                        "departureReal": null,
                        "arrivalScheduled": "02:03",
                        "arrivalReal": null,
                        "travelTime": "03h13'",
                        "price": "69,00",
                        "trainId": "18170",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";

     public static String KG_GG = """
            {
                "scrapingId": "5ba6dad4-9abe-4dac-84a8-c73d66482546",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 15,
                        "departureScheduled": "06:57",
                        "departureReal": null,
                        "arrivalScheduled": "12:12",
                        "arrivalReal": null,
                        "travelTime": "5h15",
                        "price": "225,00 zł",
                        "trainId": "3112, 4508",
                        "routeSections": [],
                        "carriers": [
                            "EIP",
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 16,
                        "departureScheduled": "05:50",
                        "departureReal": null,
                        "arrivalScheduled": "11:06",
                        "arrivalReal": null,
                        "travelTime": "5h16",
                        "price": "225,00 zł",
                        "trainId": "3510",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 17,
                        "departureScheduled": "17:56",
                        "departureReal": null,
                        "arrivalScheduled": "23:12",
                        "arrivalReal": null,
                        "travelTime": "5h16",
                        "price": "191,00 zł",
                        "trainId": "3150, 4500",
                        "routeSections": [],
                        "carriers": [
                            "EIC",
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 18,
                        "departureScheduled": "22:00",
                        "departureReal": null,
                        "arrivalScheduled": "06:01",
                        "arrivalReal": null,
                        "travelTime": "8h01",
                        "price": "89,00 zł",
                        "trainId": "38170",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 19,
                        "departureScheduled": "19:52",
                        "departureReal": null,
                        "arrivalScheduled": "04:53",
                        "arrivalReal": null,
                        "travelTime": "9h01",
                        "price": "94,00 zł",
                        "trainId": "36172",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 20,
                        "departureScheduled": "00:30",
                        "departureReal": null,
                        "arrivalScheduled": "07:58",
                        "arrivalReal": null,
                        "travelTime": "7h28",
                        "price": "92,00 zł",
                        "trainId": "35170",
                        "routeSections": [],
                        "carriers": [
                            "TLK"
                        ],
                        "delayed": false
                    }
                ],
                "reason": null
            }""";
     public static String KG_GW = """
            {
                "scrapingId": "8b7a16b1-61b2-4498-bfb0-9f50391f7449",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 21,
                        "departureScheduled": "00:30",
                        "departureReal": null,
                        "arrivalScheduled": "08:06",
                        "arrivalReal": null,
                        "travelTime": "07h36'",
                        "price": "97,50",
                        "trainId": "35170, 96307",
                        "routeSections": [],
                        "carriers": [
                            "TLK",
                            "R"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 22,
                        "departureScheduled": "04:12",
                        "departureReal": null,
                        "arrivalScheduled": "11:39",
                        "arrivalReal": null,
                        "travelTime": "07h27'",
                        "price": "95,00",
                        "trainId": "54, 6504",
                        "routeSections": [],
                        "carriers": [
                            "IC",
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 23,
                        "departureScheduled": "05:50",
                        "departureReal": null,
                        "arrivalScheduled": "11:11",
                        "arrivalReal": null,
                        "travelTime": "05h21'",
                        "price": "225,00",
                        "trainId": "3510",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 24,
                        "departureScheduled": "00:30",
                        "departureReal": null,
                        "arrivalScheduled": "08:09",
                        "arrivalReal": null,
                        "travelTime": "7h39",
                        "price": "97,50 zł",
                        "trainId": "35170, 95729",
                        "routeSections": [],
                        "carriers": [
                            "TLK",
                            "SKM-T"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 25,
                        "departureScheduled": "17:56",
                        "departureReal": null,
                        "arrivalScheduled": "23:17",
                        "arrivalReal": null,
                        "travelTime": "5h21",
                        "price": "191,00 zł",
                        "trainId": "3150, 4500",
                        "routeSections": [],
                        "carriers": [
                            "EIC",
                            "EIP"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 26,
                        "departureScheduled": "22:00",
                        "departureReal": null,
                        "arrivalScheduled": "06:08",
                        "arrivalReal": null,
                        "travelTime": "8h 8min",
                        "price": "89,00 PLN",
                        "trainId": "38170",
                        "routeSections": [
                            {
                                "id": 1,
                                "sectionName": "Kraków Gł. -> Gdańsk Wrzeszcz",
                                "classAvailabilities": [
                                    {
                                        "id": 1,
                                        "className": "Class 1",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 2,
                                        "className": "Class 2",
                                        "availability": "Brak wolnych miejsc",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 27,
                        "departureScheduled": "19:52",
                        "departureReal": null,
                        "arrivalScheduled": "05:00",
                        "arrivalReal": null,
                        "travelTime": "9h 8min",
                        "price": "124,00 PLN",
                        "trainId": "36172",
                        "routeSections": [
                            {
                                "id": 2,
                                "sectionName": "Kraków Gł. -> Gdańsk Wrzeszcz",
                                "classAvailabilities": [
                                    {
                                        "id": 3,
                                        "className": "Class 1",
                                        "availability": "Brak wolnych miejsc",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 4,
                                        "className": "Class 2",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 28,
                        "departureScheduled": "00:30",
                        "departureReal": null,
                        "arrivalScheduled": "08:10",
                        "arrivalReal": null,
                        "travelTime": "07h40'",
                        "price": "92,00",
                        "trainId": "35170",
                        "routeSections": [],
                        "carriers": [
                            "TLK"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";
     public static String KG_WC = """
            {
                "scrapingId": "411a8774-9a76-4e30-bcad-a822ecb0b0ee",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 29,
                        "departureScheduled": "19:04",
                        "departureReal": null,
                        "arrivalScheduled": "22:38",
                        "arrivalReal": null,
                        "travelTime": "3h 34min",
                        "price": "72,00 PLN",
                        "trainId": "3128, 117",
                        "routeSections": [
                            {
                                "id": 3,
                                "sectionName": "Kraków Gł. -> Zawiercie",
                                "classAvailabilities": [
                                    {
                                        "id": 5,
                                        "className": "Class 1",
                                        "availability": "Last available seats",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 6,
                                        "className": "Class 2",
                                        "availability": "Brak wolnych miejsc",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            },
                            {
                                "id": 4,
                                "sectionName": "Zawiercie -> Warszawa Centr.",
                                "classAvailabilities": [
                                    {
                                        "id": 7,
                                        "className": "Class 1",
                                        "availability": "No information on seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 8,
                                        "className": "Class 2",
                                        "availability": "No information on seat availability",
                                        "specialSeatInfo": "no information"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC",
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 30,
                        "departureScheduled": "20:13",
                        "departureReal": null,
                        "arrivalScheduled": "22:46",
                        "arrivalReal": null,
                        "travelTime": "02h33'",
                        "price": "68,00",
                        "trainId": "31100",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 31,
                        "departureScheduled": "18:58",
                        "departureReal": null,
                        "arrivalScheduled": "21:20",
                        "arrivalReal": null,
                        "travelTime": "02h22'",
                        "price": "169,00",
                        "trainId": "3102",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 32,
                        "departureScheduled": "21:30",
                        "departureReal": null,
                        "arrivalScheduled": "00:05",
                        "arrivalReal": null,
                        "travelTime": "02h35'",
                        "price": "68,00",
                        "trainId": "3124",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 33,
                        "departureScheduled": "19:57",
                        "departureReal": null,
                        "arrivalScheduled": "22:20",
                        "arrivalReal": null,
                        "travelTime": "02h23'",
                        "price": "169,00",
                        "trainId": "3100",
                        "routeSections": [],
                        "carriers": [
                            "EIP"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 34,
                        "departureScheduled": "19:04",
                        "departureReal": null,
                        "arrivalScheduled": "22:50",
                        "arrivalReal": null,
                        "travelTime": "3h 46min",
                        "price": "70,00 PLN",
                        "trainId": "3120",
                        "routeSections": [
                            {
                                "id": 5,
                                "sectionName": "Kraków Gł. -> Warszawa Centr.",
                                "classAvailabilities": [
                                    {
                                        "id": 9,
                                        "className": "Class 1",
                                        "availability": "Last available seats",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 10,
                                        "className": "Class 2",
                                        "availability": "Brak wolnych miejsc",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 35,
                        "departureScheduled": "17:56",
                        "departureReal": null,
                        "arrivalScheduled": "20:20",
                        "arrivalReal": null,
                        "travelTime": "2h24",
                        "price": "149,00 zł",
                        "trainId": "3150",
                        "routeSections": [],
                        "carriers": [
                            "EIC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 36,
                        "departureScheduled": "18:06",
                        "departureReal": null,
                        "arrivalScheduled": "20:46",
                        "arrivalReal": null,
                        "travelTime": "2h40",
                        "price": "68,00 zł",
                        "trainId": "4160",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    }
                ],
                "reason": null
            }""";
     public static String KG_PG = """
            {
                "scrapingId": "42a2edcf-69e9-432d-90d4-a596cee1c949",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 37,
                        "departureScheduled": "17:55",
                        "departureReal": null,
                        "arrivalScheduled": "23:37",
                        "arrivalReal": null,
                        "travelTime": "5h42",
                        "price": "77,00 zł",
                        "trainId": "36101, 37150",
                        "routeSections": [],
                        "carriers": [
                            "IC",
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 38,
                        "departureScheduled": "04:12",
                        "departureReal": null,
                        "arrivalScheduled": "08:30",
                        "arrivalReal": null,
                        "travelTime": "04h18'",
                        "price": "77,00",
                        "trainId": "54, 6504",
                        "routeSections": [],
                        "carriers": [
                            "IC",
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 39,
                        "departureScheduled": "00:30",
                        "departureReal": null,
                        "arrivalScheduled": "07:24",
                        "arrivalReal": null,
                        "travelTime": "06h54'",
                        "price": "170,00",
                        "trainId": "35170, 248",
                        "routeSections": [],
                        "carriers": [
                            "TLK",
                            "EIC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 40,
                        "departureScheduled": "00:30",
                        "departureReal": null,
                        "arrivalScheduled": "08:23",
                        "arrivalReal": null,
                        "travelTime": "07h53'",
                        "price": "139,20",
                        "trainId": "35170, 19999, 1806",
                        "routeSections": [],
                        "carriers": [
                            "TLK",
                            "ŁKABUS",
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 41,
                        "departureScheduled": "20:13",
                        "departureReal": null,
                        "arrivalScheduled": "02:03",
                        "arrivalReal": null,
                        "travelTime": "05h50'",
                        "price": "86,00",
                        "trainId": "31100, 18170",
                        "routeSections": [],
                        "carriers": [
                            "IC",
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 42,
                        "departureScheduled": "17:36",
                        "departureReal": null,
                        "arrivalScheduled": "22:27",
                        "arrivalReal": null,
                        "travelTime": "4h51",
                        "price": "77,00 zł",
                        "trainId": "3724",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 43,
                        "departureScheduled": "19:52",
                        "departureReal": null,
                        "arrivalScheduled": "01:21",
                        "arrivalReal": null,
                        "travelTime": "05h29'",
                        "price": "",
                        "trainId": "36172",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 44,
                        "departureScheduled": "22:36",
                        "departureReal": null,
                        "arrivalScheduled": "04:50",
                        "arrivalReal": null,
                        "travelTime": "06h14'",
                        "price": "76,00",
                        "trainId": "38172",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";
     public static String PG_GG = """
            {
                "scrapingId": "9e87fb2c-a3b6-4cc7-a19f-46c2ece0ee80",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 45,
                        "departureScheduled": "17:40",
                        "departureReal": null,
                        "arrivalScheduled": "20:23",
                        "arrivalReal": null,
                        "travelTime": "2h43",
                        "price": "70,00 zł",
                        "trainId": "231",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 46,
                        "departureScheduled": "18:40",
                        "departureReal": null,
                        "arrivalScheduled": "21:43",
                        "arrivalReal": null,
                        "travelTime": "03h03'",
                        "price": "",
                        "trainId": "65100",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 47,
                        "departureScheduled": "19:40",
                        "departureReal": null,
                        "arrivalScheduled": "23:00",
                        "arrivalReal": null,
                        "travelTime": "3h 20min",
                        "price": "70,00 PLN",
                        "trainId": "75108",
                        "routeSections": [
                            {
                                "id": 6,
                                "sectionName": "Poznań Gł. -> Gdańsk Gł.",
                                "classAvailabilities": [
                                    {
                                        "id": 11,
                                        "className": "Class 1",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 12,
                                        "className": "Class 2",
                                        "availability": "Last available seats",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 48,
                        "departureScheduled": "06:40",
                        "departureReal": null,
                        "arrivalScheduled": "09:36",
                        "arrivalReal": null,
                        "travelTime": "02h56'",
                        "price": "70,00",
                        "trainId": "6500",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 49,
                        "departureScheduled": "05:09",
                        "departureReal": null,
                        "arrivalScheduled": "08:06",
                        "arrivalReal": null,
                        "travelTime": "02h57'",
                        "price": "70,00",
                        "trainId": "7500",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 50,
                        "departureScheduled": "20:40",
                        "departureReal": null,
                        "arrivalScheduled": "23:27",
                        "arrivalReal": null,
                        "travelTime": "2h 47min",
                        "price": "70,00 PLN",
                        "trainId": "260",
                        "routeSections": [
                            {
                                "id": 7,
                                "sectionName": "Poznań Gł. -> Gdańsk Gł.",
                                "classAvailabilities": [
                                    {
                                        "id": 13,
                                        "className": "Class 1",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 14,
                                        "className": "Class 2",
                                        "availability": "Last available seats",
                                        "specialSeatInfo": "no information"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 51,
                        "departureScheduled": "01:41",
                        "departureReal": null,
                        "arrivalScheduled": "04:53",
                        "arrivalReal": null,
                        "travelTime": "03h12'",
                        "price": "59,50",
                        "trainId": "460",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";
    public static String PG_GW = """
            {
                "scrapingId": "f6370395-9f70-4d1f-8f98-5196c9d89716",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 52,
                        "departureScheduled": "17:40",
                        "departureReal": null,
                        "arrivalScheduled": "20:30",
                        "arrivalReal": null,
                        "travelTime": "2h50",
                        "price": "70,00 zł",
                        "trainId": "231",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 53,
                        "departureScheduled": "18:40",
                        "departureReal": null,
                        "arrivalScheduled": "21:50",
                        "arrivalReal": null,
                        "travelTime": "03h10'",
                        "price": "",
                        "trainId": "65100",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 54,
                        "departureScheduled": "19:40",
                        "departureReal": null,
                        "arrivalScheduled": "23:07",
                        "arrivalReal": null,
                        "travelTime": "3h 27min",
                        "price": "70,00 PLN",
                        "trainId": "75108",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 55,
                        "departureScheduled": "06:40",
                        "departureReal": null,
                        "arrivalScheduled": "09:43",
                        "arrivalReal": null,
                        "travelTime": "03h03'",
                        "price": "70,00",
                        "trainId": "6500",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 56,
                        "departureScheduled": "05:09",
                        "departureReal": null,
                        "arrivalScheduled": "08:15",
                        "arrivalReal": null,
                        "travelTime": "03h06'",
                        "price": "70,00",
                        "trainId": "7500",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 57,
                        "departureScheduled": "20:40",
                        "departureReal": null,
                        "arrivalScheduled": "23:34",
                        "arrivalReal": null,
                        "travelTime": "2h 54min",
                        "price": "70,00 PLN",
                        "trainId": "260",
                        "routeSections": [
                            {
                                "id": 8,
                                "sectionName": "Poznań Gł. -> Gdańsk Wrzeszcz",
                                "classAvailabilities": [
                                    {
                                        "id": 15,
                                        "className": "Class 1",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 16,
                                        "className": "Class 2",
                                        "availability": "Last available seats",
                                        "specialSeatInfo": "no information"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 58,
                        "departureScheduled": "01:41",
                        "departureReal": null,
                        "arrivalScheduled": "05:00",
                        "arrivalReal": null,
                        "travelTime": "03h19'",
                        "price": "59,50",
                        "trainId": "460",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";
    public static String PG_WC = """
            {
                "scrapingId": "324a1c21-f990-4a98-b438-d01ff4e7ee7d",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 59,
                        "departureScheduled": "17:45",
                        "departureReal": null,
                        "arrivalScheduled": "20:30",
                        "arrivalReal": null,
                        "travelTime": "2h45",
                        "price": "69,00 zł",
                        "trainId": "7202",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 60,
                        "departureScheduled": "18:35",
                        "departureReal": null,
                        "arrivalScheduled": "21:00",
                        "arrivalReal": null,
                        "travelTime": "2h25",
                        "price": "149,00 zł",
                        "trainId": "247",
                        "routeSections": [],
                        "carriers": [
                            "EIC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 61,
                        "departureScheduled": "19:37",
                        "departureReal": null,
                        "arrivalScheduled": "22:30",
                        "arrivalReal": null,
                        "travelTime": "2h 53min",
                        "price": "69,00 PLN",
                        "trainId": "8106",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 62,
                        "departureScheduled": "20:40",
                        "departureReal": null,
                        "arrivalScheduled": "03:45",
                        "arrivalReal": null,
                        "travelTime": "7h 5min",
                        "price": "85,00 PLN",
                        "trainId": "260, 83170",
                        "routeSections": [
                            {
                                "id": 9,
                                "sectionName": "Poznań Gł. -> Tczew",
                                "classAvailabilities": [
                                    {
                                        "id": 17,
                                        "className": "Class 1",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 18,
                                        "className": "Class 2",
                                        "availability": "Last available seats",
                                        "specialSeatInfo": "no information"
                                    }
                                ]
                            },
                            {
                                "id": 10,
                                "sectionName": "Tczew -> Warszawa Centr.",
                                "classAvailabilities": [
                                    {
                                        "id": 19,
                                        "className": "Class 1",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 20,
                                        "className": "Class 2",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC",
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 63,
                        "departureScheduled": "17:40",
                        "departureReal": null,
                        "arrivalScheduled": "19:59",
                        "arrivalReal": null,
                        "travelTime": "2h19",
                        "price": "149,00 zł",
                        "trainId": "8104",
                        "routeSections": [],
                        "carriers": [
                            "EIC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 64,
                        "departureScheduled": "20:35",
                        "departureReal": null,
                        "arrivalScheduled": "23:00",
                        "arrivalReal": null,
                        "travelTime": "2h 25min",
                        "price": "149,00 PLN",
                        "trainId": "249",
                        "routeSections": [
                            {
                                "id": 11,
                                "sectionName": "Poznań Gł. -> Warszawa Centr.",
                                "classAvailabilities": [
                                    {
                                        "id": 21,
                                        "className": "Class 1",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 22,
                                        "className": "Class 2",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "EIC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 65,
                        "departureScheduled": "05:46",
                        "departureReal": null,
                        "arrivalScheduled": "08:30",
                        "arrivalReal": null,
                        "travelTime": "02h44'",
                        "price": "69,00",
                        "trainId": "72100",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 66,
                        "departureScheduled": "22:18",
                        "departureReal": null,
                        "arrivalScheduled": "04:50",
                        "arrivalReal": null,
                        "travelTime": "06h32'",
                        "price": "99,70",
                        "trainId": "77592, 61170",
                        "routeSections": [],
                        "carriers": [
                            "KW",
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 67,
                        "departureScheduled": "03:16",
                        "departureReal": null,
                        "arrivalScheduled": "06:30",
                        "arrivalReal": null,
                        "travelTime": "03h14'",
                        "price": "69,00",
                        "trainId": "81170",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";
    public static String PG_KG = """
            {
                "scrapingId": "a3ea7f83-00c7-482b-bc01-7145d030fb93",
                "status": "COMPLETED",
                "results": [
                    {
                        "id": 68,
                        "departureScheduled": "20:35",
                        "departureReal": null,
                        "arrivalScheduled": "03:40",
                        "arrivalReal": null,
                        "travelTime": "7h 5min",
                        "price": "171,00 PLN",
                        "trainId": "249, 53170",
                        "routeSections": [
                            {
                                "id": 12,
                                "sectionName": "Poznań Gł. -> Warszawa Zach.",
                                "classAvailabilities": [
                                    {
                                        "id": 23,
                                        "className": "Class 1",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 24,
                                        "className": "Class 2",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            },
                            {
                                "id": 13,
                                "sectionName": "Warszawa Zach. -> Kraków Gł.",
                                "classAvailabilities": [
                                    {
                                        "id": 25,
                                        "className": "Class 1",
                                        "availability": "High seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 26,
                                        "className": "Class 2",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "EIC",
                            "TLK"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 69,
                        "departureScheduled": "03:16",
                        "departureReal": null,
                        "arrivalScheduled": "09:06",
                        "arrivalReal": null,
                        "travelTime": "05h50'",
                        "price": "188,00",
                        "trainId": "81170, 1302",
                        "routeSections": [],
                        "carriers": [
                            "IC",
                            "EIP"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 70,
                        "departureScheduled": "19:31",
                        "departureReal": null,
                        "arrivalScheduled": "23:46",
                        "arrivalReal": null,
                        "travelTime": "04h15'",
                        "price": "77,00",
                        "trainId": "5604, 55",
                        "routeSections": [],
                        "carriers": [
                            "IC",
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 71,
                        "departureScheduled": "05:38",
                        "departureReal": null,
                        "arrivalScheduled": "10:27",
                        "arrivalReal": null,
                        "travelTime": "04h49'",
                        "price": "76,00",
                        "trainId": "73150, 63100",
                        "routeSections": [],
                        "carriers": [
                            "IC",
                            "IC"
                        ],
                        "delayed": true
                    },
                    {
                        "id": 72,
                        "departureScheduled": "23:11",
                        "departureReal": null,
                        "arrivalScheduled": "05:25",
                        "arrivalReal": null,
                        "travelTime": "6h 14min",
                        "price": "76,00 PLN",
                        "trainId": "83172",
                        "routeSections": [
                            {
                                "id": 14,
                                "sectionName": "Poznań Gł. -> Kraków Gł.",
                                "classAvailabilities": [
                                    {
                                        "id": 27,
                                        "className": "Class 1",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "no information"
                                    },
                                    {
                                        "id": 28,
                                        "className": "Class 2",
                                        "availability": "Limited seat availability",
                                        "specialSeatInfo": "A special seat is available"
                                    }
                                ]
                            }
                        ],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": false
                    },
                    {
                        "id": 73,
                        "departureScheduled": "02:50",
                        "departureReal": null,
                        "arrivalScheduled": "08:47",
                        "arrivalReal": null,
                        "travelTime": "05h57'",
                        "price": "77,00",
                        "trainId": "461",
                        "routeSections": [],
                        "carriers": [
                            "IC"
                        ],
                        "delayed": true
                    }
                ],
                "reason": null
            }""";

}
