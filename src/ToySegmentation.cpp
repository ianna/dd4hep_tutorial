#include "ToySegmentation.h"
#include <climits>
#include <cmath>
#include <stdexcept>

namespace dd4hep {
namespace DDSegmentation {

ToySegmentation::ToySegmentation(const std::string& cellEncoding) : Segmentation(cellEncoding) {
    _type = "ToySegmentation";
    _description = "Toy segmentation";
    registerIdentifier("identifier_system", "Cell ID identifier for System", fSystemId, "system");
    registerIdentifier("identifier_phi",    "Cell ID identifier for Phi",    fPhiId,    "phi");
    registerIdentifier("identifier_theta",  "Cell ID identifier for Theta",  fThetaId,  "theta");
    registerIdentifier("identifier_depth",  "Cell ID identifier for Depth",  fDepthId,  "depth");
}

ToySegmentation::ToySegmentation(const BitFieldCoder* decoder) : Segmentation(decoder) {
    _type = "ToySegmentation";
    _description = "Toy segmentation";
    registerIdentifier("identifier_system", "Cell ID identifier for System", fSystemId, "system");
    registerIdentifier("identifier_phi",    "Cell ID identifier for Phi",    fPhiId,    "phi");
    registerIdentifier("identifier_theta",  "Cell ID identifier for Theta",  fThetaId,  "theta");
    registerIdentifier("identifier_depth",  "Cell ID identifier for Depth",  fDepthId,  "depth");
}

ToySegmentation::~ToySegmentation() {}

Vector3D ToySegmentation::position(const CellID& cID) const {
    if (fPositionOf.find(cID) != fPositionOf.end()) {
        return fPositionOf.find(cID)->second;
    }
    return Vector3D(0,0,0);
};


}
}
