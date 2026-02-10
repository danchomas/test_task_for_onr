cmake_minimum_required(VERSION 3.14)
project(result)

set(CMAKE_CXX_STANDARD 17)

include(FetchContent)
FetchContent_Declare(
    json
    GIT_REPOSITORY https://github.com/nlohmann/json.git
    GIT_TAG v3.11.2
)
FetchContent_MakeAvailable(json)

add_executable(result 
    main.cpp 
    product.cpp 
    buy.cpp 
    check.cpp
)
target_link_libraries(result PRIVATE nlohmann_json::nlohmann_json)