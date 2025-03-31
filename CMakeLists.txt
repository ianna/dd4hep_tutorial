cmake_minimum_required(VERSION 3.8 FATAL_ERROR)

SET(PackageName ToyCalorimeter)
PROJECT(${PackageName})

set(CMAKE_CXX_STANDARD 17)
include(GNUInstallDirs)
set(CMAKE_INSTALL_LIBDIR lib)

IF(NOT TARGET DD4hep::DDCore)
  find_package ( DD4hep REQUIRED )
  include ( ${DD4hep_DIR}/cmake/DD4hep.cmake )
  include ( ${DD4hep_DIR}/cmake/DD4hepBuild.cmake )
  dd4hep_configure_output()
ENDIF()

dd4hep_set_compiler_flags()

find_package(ROOT REQUIRED)
find_package(Geant4 REQUIRED)
find_package(podio REQUIRED HINTS $ENV{PODIO})
find_package(EDM4HEP REQUIRED HINTS $ENV{EDM4hep})

add_subdirectory(edm4toy)

if (DD4HEP_USE_GEANT4)
  dd4hep_add_dictionary(
    G__ToyCalorimeter
    USE_COMMAND_TO_GENERATE
    SOURCES ${DD4hep_DIR}/include/ROOT/Warnings.h include/ToyCaloHit.h 
    LINKDEF ${DD4hep_DIR}/include/ROOT/LinkDef.h
    OUTPUT  ${LIBRARY_OUTPUT_PATH}
    USES    DD4hep::DDCore DD4hep::DDG4 Geant4::Interface
  )
endif()

dd4hep_configure_output()

set(BOOST_ROOT "$ENV{BOOST_ROOT}")

file(GLOB sources
  ${PROJECT_SOURCE_DIR}/src/*.cpp
)
file(GLOB headers
  ${PROJECT_SOURCE_DIR}/include/*.h
)

dd4hep_add_plugin (
  ToyCalorimeter
  GENERATED G__ToyCalorimeter.cxx 
  SOURCES ${sources}
  USES    DD4hep::DDCore 
          DD4hep::DDAlign 
          DD4hep::DDCond 
          DD4hep::DDG4 
          ROOT::Core 
          ROOT::Geom 
          ROOT::GenVector 
          ROOT::MathCore
          CLHEP::CLHEP 
          Geant4::Interface
          EDM4HEP::edm4hep
          EDM4HEP::edm4hepDict
          podio::podio
          podio::podioDict
          podio::podioRootIO
          edm4toy
          edm4toy::edm4toyDict
)

target_include_directories(ToyCalorimeter PUBLIC include)
target_link_options(ToyCalorimeter PRIVATE -L${Geant4_DIR}/..)
install(TARGETS ToyCalorimeter LIBRARY DESTINATION lib)
dd4hep_instantiate_package(${PackageName})
