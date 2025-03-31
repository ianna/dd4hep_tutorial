#include <DD4hep/Printout.h>
#include <DD4hep/InstanceCount.h>
#include <DDG4/Geant4Data.h>
#include "ToyCaloHit.h"

ToyCalorimeter::ToyCaloHit::ToyCaloHit():
  Geant4HitData(),
  position(),
  truth(),
  energyDeposit(0),
  yourInterestingQuantity(0)
{
  dd4hep::InstanceCount::increment(this);
}

ToyCalorimeter::ToyCaloHit::ToyCaloHit(const Position& pos):
  Geant4HitData(),
  position(pos),
  truth(),
  energyDeposit(0),
  yourInterestingQuantity(0)
{
  dd4hep::InstanceCount::increment(this);
}

ToyCalorimeter::ToyCaloHit::~ToyCaloHit() {
  dd4hep::InstanceCount::decrement(this);
}