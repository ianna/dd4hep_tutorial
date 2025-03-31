#ifndef ToySegmentation_h
#define ToySegmentation_h 1
#include "DDSegmentation/Segmentation.h"
#include "Math/Vector3D.h"
#include "DD4hep/DetFactoryHelper.h"
#include <vector>
#include <cmath>
#include <climits>

namespace dd4hep {
namespace DDSegmentation {

class ToySegmentation : public Segmentation {
    public:
        ToySegmentation(const std::string& aCellEncoding);
        ToySegmentation(const BitFieldCoder* decoder);
        virtual ~ToySegmentation() override;

        virtual Vector3D position(const CellID& aCellID) const override;

        CellID cellID(const Vector3D& /*localPosition*/, 
            const Vector3D& /*globalPosition*/, 
            const VolumeID& vID) const override {
            return setCellID(System(vID), Phi(vID), Theta(vID), Depth(vID) );
        }

        VolumeID setVolumeID(int System, int Phi, int Theta, int Depth) const {
            VolumeID SystemId = static_cast<VolumeID>(System);
            VolumeID PhiId = static_cast<VolumeID>(Phi);
            VolumeID ThetaId = static_cast<VolumeID>(Theta);
            VolumeID DepthId = static_cast<VolumeID>(Depth);
            VolumeID vID = 0;
            _decoder->set(vID, fSystemId, SystemId);
            _decoder->set(vID, fPhiId, PhiId);
            _decoder->set(vID, fThetaId, ThetaId);
            _decoder->set(vID, fDepthId, DepthId);
            return vID;
        }

        CellID setCellID(int System, int Phi, int Theta, int Depth) const {
            VolumeID SystemId = static_cast<VolumeID>(System);
            VolumeID PhiId = static_cast<VolumeID>(Phi);
            VolumeID ThetaId = static_cast<VolumeID>(Theta);
            VolumeID DepthId = static_cast<VolumeID>(Depth);
            VolumeID vID = 0;
            _decoder->set(vID, fSystemId, SystemId);
            _decoder->set(vID, fPhiId, PhiId);
            _decoder->set(vID, fThetaId, ThetaId);
            _decoder->set(vID, fDepthId, DepthId);
            return vID;
        }
        
        int System(const CellID& aCellID) const {
            VolumeID System = static_cast<VolumeID>(_decoder->get(aCellID, fSystemId));
            return static_cast<int>(System);
        }
        
        int Phi(const CellID& aCellID) const {
            VolumeID Phi = static_cast<VolumeID>(_decoder->get(aCellID, fPhiId));
            return static_cast<int>(Phi);
        }
        
        int Theta(const CellID& aCellID) const {
            VolumeID Theta = static_cast<VolumeID>(_decoder->get(aCellID, fThetaId));
            return static_cast<int>(Theta);
        }
        
        int Depth(const CellID& aCellID) const {
            VolumeID Depth = static_cast<VolumeID>(_decoder->get(aCellID, fDepthId));
            return static_cast<int>(Depth);
        }

        int getFirst32bits(const CellID& aCellID) const { return (int)aCellID; }
        int getLast32bits(const CellID& aCellID) const {
            CellID aId64 = aCellID >> sizeof(int)*CHAR_BIT;
            int aId32 = (int)aId64;
            return aId32;
        }

        CellID convertFirst32to64(const int aId32) const { return (CellID)aId32; }
        CellID convertLast32to64(const int aId32) const {
            CellID aId64 = (CellID)aId32;
            aId64 <<= sizeof(int)*CHAR_BIT;
            return aId64;
        }

        int System(const int& aId32) const { return System( convertFirst32to64(aId32) ); }
        int Phi(const int& aId32) const { return Phi( convertFirst32to64(aId32) ); }
        int Theta(const int& aId32) const { return Theta( convertFirst32to64(aId32) ); }
        int Depth(const int& aId32) const { return Depth( convertFirst32to64(aId32) ); }

        inline void savePosition(int volID_32, Vector3D pos) {fPositionOf.emplace(volID_32,pos);}

    // Define the fields for the cellId
    protected:
        std::string fSystemId;
        std::string fPhiId;
        std::string fThetaId;
        std::string fDepthId;

    // Lookup map to store cellIds and their positions
    private:
        mutable std::unordered_map<int, Vector3D> fPositionOf;

};
}
}

#endif
