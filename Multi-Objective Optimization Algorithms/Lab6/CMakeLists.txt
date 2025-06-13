cmake_minimum_required(VERSION 3.10)
project(ParadiseoSample)

set(CMAKE_CXX_STANDARD 17)

set(PARADISEO_ROOT "~/Desktop/C/Libs/paradiseo-3.1.3")
set(EIGEN3_INCLUDE_DIR "usr/include/eigen3")

include_directories(
    ${PARADISEO_ROOT}/eo/src
    ${PARADISEO_ROOT}/eo/src/es
    ${PARADISEO_ROOT}/eo/src/ga
    ${PARADISEO_ROOT}/moeo/src
    ${PARADISEO_ROOT}/mo/src
    ${EIGEN3_INCLUDE_DIR}
)

link_directories(${PARADISEO_ROOT}/build/lib)

add_definitions(-DWITH_EIGEN=1)

add_executable(MOOA6 MOOA6.cpp)

target_link_libraries(MOOA6
    eo
    eoutils
    es
    moeo
)