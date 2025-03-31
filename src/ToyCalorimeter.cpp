#include "ToySegmentationHandle.h"
#include "DD4hep/DetFactoryHelper.h"
#include "DD4hep/Printout.h"
#include "DD4hep/Shapes.h"
#include "DD4hep/Volumes.h"
#include "DD4hep/DetElement.h"
#include "DD4hep/OpticalSurfaces.h"   // If you want to use optical surfaces
#include "DD4hep/Objects.h"

using ROOT::Math::RotationY;
using ROOT::Math::RotationZ;
using ROOT::Math::XYZVector;
using namespace std;
using namespace dd4hep;


static Ref_t create_toy_calorimeter(Detector& theDetector, xml_h xmlElement, SensitiveDetector sens) {

  // ----------------------------------------------------------------
  // Load the XML elements and initialize the detector
  // ----------------------------------------------------------------

  // Handle to the XML <detector> node
  xml_det_t  detectorXML                 =xmlElement;
  
  // Handle to custom XML elements like <dim>, <barrel>, etc.
  xml_comp_t dimXML                      =detectorXML.child(_Unicode(dim));
  xml_comp_t boxXML                      =detectorXML.child(_Unicode(box));

  std::string detName                    =detectorXML.nameStr();
  int detId                              =detectorXML.id();

  const double  PHI_SEGMENTS             =dimXML.attr<double>(_Unicode(phiSegments));
  const double  BARREL_HALF_Z            =dimXML.attr<double>(_Unicode(barrelHalfZ));
  const double  BARREL_INNER_R           =dimXML.attr<double>(_Unicode(barrelInnerR));
  const double  BARREL_OUTER_R           =dimXML.attr<double>(_Unicode(barrelOuterR));

  const double  BOX_HALF_X               =boxXML.attr<double>(_Unicode(boxHalfX));
  const double  BOX_HALF_Y               =boxXML.attr<double>(_Unicode(boxHalfY));
  const double  BOX_HALF_Z               =boxXML.attr<double>(_Unicode(boxHalfZ));

  // Initialize the top-level detector element
  dd4hep::DetElement calorimeterDet(detName, detId );

  // Get the world volume and call it experimentalHall
  dd4hep::Volume experimentalHall=theDetector.pickMotherVolume(calorimeterDet);
  
  // Get the sensitive volume type
  dd4hep::xml::Dimension sdType=detectorXML.child(_Unicode(sensitive));
  
  // Set the sensitive detector type ("calorimeter", "tracker", etc.) for the volumes to be tagged as sensitive
  sens.setType(sdType.typeStr());

  // Get the segmentation type from the readout
  dd4hep::Readout readout=sens.readout();
  dd4hep::Segmentation geomseg=readout.segmentation();
  dd4hep::Segmentation* _geoSeg=&geomseg;
  auto segmentation=dynamic_cast<dd4hep::DDSegmentation::ToySegmentation *>(_geoSeg->segmentation());

  // ----------------------------------------------------------------
  // Create a global assembly volume for the calorimeter
  // ----------------------------------------------------------------
  double rmin = BARREL_INNER_R;
  double rmax = BARREL_OUTER_R;
  double dz   = BARREL_HALF_Z;

  // First create a shape, then make a volume from it
  dd4hep::Tube globalTubeShape(rmin, rmax, dz);
  dd4hep::Volume globalTubeVolume("globalTubeVolume", globalTubeShape, theDetector.material("Vacuum"));

  // Set visualization attributes for the volume
  globalTubeVolume.setVisAttributes(theDetector, detectorXML.visStr());

  // Make a placed instance of the volume
  dd4hep::PlacedVolume globalTubePlacedVol = experimentalHall.placeVolume(globalTubeVolume);

  // Set the volume ID for the placed volume
  globalTubePlacedVol.addPhysVolID("system", detId );

  // Use the global assembly volume as the placement for the calorimeter detector element
  calorimeterDet.setPlacement(globalTubePlacedVol);   

  // ----------------------------------------------------------------
  // Construct the detector by making shapes, volume, and placed volumes
  // 
  // Example shape declarations are provided below.
  // Make a toy geometry using these shapes and implement volumes and placed volumes from them.
  // Define dimensions and parameters as necessary for your geometry in the XML and import them in above.
  // Consult the ROOT docs for information on how shapes are defined
  // e.g. https://root.cern/doc/master/classTGeoPgon.html
  //
  // Make sure to calculate dimensions to make sure volumes do not overlap or protrude!
  // ----------------------------------------------------------------

  // dd4hep::Box exampleBox(10.0, 20.0, 30.0);              // half-lengths in x, y, z
  // dd4hep::Tube exampleTube(5.0, 10.0, 15.0);             // inner radius, outer radius, half-length
  // dd4hep::Cone exampleCone(15.0, 5.0, 10.0, 7.0, 12.0);  // halfZ, rmin1, rmax1, rmin2, rmax2

  // Set up materials
  Material ironMaterial    = theDetector.material("Iron");
  Material crystalMaterial = theDetector.material("PbWO4");
  Material siliconMaterial = theDetector.material("Silicon");

  // Make a box shape and volume
  dd4hep::Box aBoxShape(BOX_HALF_X, BOX_HALF_Y, BOX_HALF_Z);
  dd4hep::Volume aBoxVolume("aBoxVolume", aBoxShape, crystalMaterial);

  // Set visualization attributes for the box
  aBoxVolume.setVisAttributes(theDetector, boxXML.visStr());
  
  // Make the box a sensitive volume
  aBoxVolume.setSensitiveDetector(sens);

  // Make placements of the box in phi
  int nPhi = PHI_SEGMENTS;
  for (int i=0; i<nPhi; i++) {
    double phi      = i*(2*M_PI/nPhi);
    double dispX     = (rmin + 0.5*(rmax-rmin)) * cos(phi);
    double dispY     = (rmin + 0.5*(rmax-rmin)) * sin(phi);
    double dispZ     = 0.0;

    // Create a new transformation for each instance (rotation + translation)
    RotationZ     aRotation(phi);
    Translation3D aDisplacement(dispX, dispY, dispZ);
    Transform3D   aTransform(aRotation, aDisplacement);

    auto volID   =segmentation->setVolumeID(detId,i,0,0); // system, phi, theta, depth
    int  volID_32=segmentation->getFirst32bits(volID); // Used to ensure unique copy ids in geant4

    // Make a new placed volume of exampleBoxVolume
    dd4hep::PlacedVolume aBoxPlacedVol = globalTubeVolume.placeVolume(aBoxVolume, volID_32, aTransform);

    // PhysVolID is used at dd4hep level, not geant4, have to repeat
    aBoxPlacedVol.addPhysVolID("system", detId);
    aBoxPlacedVol.addPhysVolID("phi", i);
    aBoxPlacedVol.addPhysVolID("theta", 0);
    aBoxPlacedVol.addPhysVolID("depth", 0);

    // Save the position of the placed volume for easy lookup when producing hits
    segmentation->savePosition(volID_32, XYZVector(dispX, dispY, dispZ)/dd4hep::mm);
  }

  return calorimeterDet;
}

//---------------------------------------------------------------------------
// Register the detector element in dd4hep
// The first argument is the name used in the XML <detector type="ToyCalorimeter">
//---------------------------------------------------------------------------
DECLARE_DETELEMENT(ToyCalorimeter, create_toy_calorimeter)
