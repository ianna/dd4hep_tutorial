find_package(EDM4HEP REQUIRED)

option(BUILD_DATA_MODEL "Run podio class generator yaml file" ON)

PODIO_GENERATE_DATAMODEL(edm4toy ../edm4toy.yaml headers sources 
  UPSTREAM_EDM edm4hep:${EDM4HEP_DATA_DIR}/edm4hep.yaml
  IO_BACKEND_HANDLERS ${PODIO_IO_HANDLERS}
)

LIST(FILTER headers EXCLUDE REGEX .*SIOBlock.h)
LIST(FILTER sources EXCLUDE REGEX .*SIOBlock.cc)

##############

add_library(edm4toy SHARED ${sources} ${headers})
target_link_libraries(edm4toy PUBLIC EDM4HEP::edm4hep
  podio::podio
)
target_include_directories(edm4toy
  PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)
set_target_properties(edm4toy PROPERTIES PUBLIC_HEADER "${headers}")

##############

PODIO_ADD_ROOT_IO_DICT(edm4toyDict edm4toy "${headers}" src/selection.xml)
add_library(edm4toy::edm4toyDict ALIAS edm4toyDict)

##############

list(APPEND edm4toy_INSTALL_LIBS edm4toy edm4toyDict)

##############

install(TARGETS ${edm4toy_INSTALL_LIBS}
  EXPORT edm4toyTargets
  RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}" COMPONENT bin
  LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}" COMPONENT shlib
  PUBLIC_HEADER DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/edm4toy" COMPONENT dev
)

install(FILES
  "${CMAKE_CURRENT_BINARY_DIR}/edm4toyDictDict.rootmap"
  DESTINATION "${CMAKE_INSTALL_LIBDIR}" COMPONENT dev
)

install(FILES
  "${CMAKE_CURRENT_BINARY_DIR}/libedm4toyDict_rdict.pcm"
  DESTINATION "${CMAKE_INSTALL_LIBDIR}" COMPONENT dev
)
