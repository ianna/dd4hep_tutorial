#ifndef ToyCaloHit_h
#define ToyCaloHit_h 1
#include "DDG4/Geant4Data.h"

namespace ToyCalorimeter {

  typedef ROOT::Math::XYZVector Position;

    class ToyCaloHit : public dd4hep::sim::Geant4HitData {

      public:
        typedef dd4hep::sim::Geant4HitData base_t;

        Position      position;
        Contributions truth;
        double        energyDeposit;

        double        yourInterestingQuantity;
        
      public:
        ToyCaloHit();
        ToyCaloHit(ToyCaloHit&& c) = delete;
        ToyCaloHit(const ToyCaloHit& c) = delete;
        ToyCaloHit(const Position& cell_pos);
        virtual ~ToyCaloHit();
        ToyCaloHit& operator=(ToyCaloHit&& c) = delete;
        ToyCaloHit& operator=(const ToyCaloHit& c) = delete;
    };

};

#endif
