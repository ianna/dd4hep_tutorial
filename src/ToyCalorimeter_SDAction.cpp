#include "ToySegmentation.h"
#include "DDG4/Geant4SensDetAction.inl"
#include "DDG4/Factories.h"
#include "G4OpticalPhoton.hh"
#include "G4VProcess.hh"

// Holder for what kind of hit type we want to use for our detector
// The built-in Geant4Calorimeter::Hit is used here
namespace ToyCalorimeter {
  class ToyCalorimeter_SDAction {
    public:
      typedef dd4hep::sim::Geant4Calorimeter::Hit Hit;
  };
}
namespace dd4hep {
  namespace sim {

    using namespace ToyCalorimeter;
    
    template <> void Geant4SensitiveAction<ToyCalorimeter_SDAction>::defineCollections()    {
      // Declare the ROOT collection (tree) for the hits
      m_collectionID = defineCollection<ToyCalorimeter_SDAction::Hit>("ToyCalorimeterHits");
    }

    template <> bool 
    Geant4SensitiveAction<ToyCalorimeter_SDAction>::process(const G4Step* step,G4TouchableHistory* /*hist*/) {
      G4StepPoint        *thePrePoint =step->GetPreStepPoint();
      G4TouchableHandle  thePreStepTouchable =thePrePoint->GetTouchableHandle();

      // Uncomment if you want to save MC step contributions
      // Geant4StepHandler h(step);
      // Geant4HitData::MonteCarloContrib contrib = Geant4HitData::extractContribution(step);

      auto cellID =thePreStepTouchable->GetCopyNumber(0);
      G4Track *track =step->GetTrack();
      
      // Get the segmentation for the sensitive detector
      dd4hep::Segmentation *_geoSeg=&m_segmentation;
      auto segmentation=dynamic_cast<dd4hep::DDSegmentation::ToySegmentation *>(_geoSeg->segmentation());

      // Get the position of the detector cell from the segmentation
      DDSegmentation::Vector3D pos =segmentation->position(cellID);
      Position global(pos.x(),pos.y(),pos.z());

      // Get the energy deposited in the step
      G4double edep =step->GetTotalEnergyDeposit();

      // Get the colletion for the hits
      Geant4HitCollection* coll =collection(m_collectionID);

      // Check if the hit already exists in the collection
      // If not, create a new hit and add it to the collection
      auto* hit =coll->findByKey<ToyCalorimeter_SDAction::Hit>(cellID);
      if(!hit) {
        hit =new ToyCalorimeter_SDAction::Hit(global);
        hit->cellID =cellID;
        coll->add(cellID, hit);
      }
      
      // Add the energy deposit to the hit if it is above a threshold (in MeV)
      if(edep>0.1) {
        hit->energyDeposit+=edep;
      }

      // Uncomment if you want to save MC step contributions
      // hit->truth.emplace_back(contrib);

      return true;
    }
  }
}

namespace dd4hep { namespace sim {
    typedef Geant4SensitiveAction<ToyCalorimeter_SDAction> ToyCalorimeter_SDAction;
}}

// Declare the sensitive action and set the name to be used in the steering file
DECLARE_GEANT4SENSITIVE(ToyCalorimeter_SDAction)