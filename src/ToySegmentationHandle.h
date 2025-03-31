#ifndef ToySegmentationHandle_h
#define ToySegmentationHandle_h 1
#include "ToySegmentation.h"
#include "DD4hep/Segmentations.h"
#include "DD4hep/detail/SegmentationsInterna.h"
#include "Math/Vector3D.h"

namespace dd4hep {
    
class Segmentation;
template <typename T>
class SegmentationWrapper;

typedef Handle<SegmentationWrapper<DDSegmentation::ToySegmentation>> ToySegmentationHandle;

class ToySegmentation : public ToySegmentationHandle {
public:
    typedef ToySegmentationHandle::Object Object;

public:
    ToySegmentation() = default;
    ToySegmentation(const ToySegmentation& e) = default;
    ToySegmentation(const Segmentation& e) : Handle<Object>(e) {}
    ToySegmentation(const Handle<Object>& e) : Handle<Object>(e) {}
    template <typename Q>
    ToySegmentation(const Handle<Q>& e) : Handle<Object>(e) {}
    ToySegmentation& operator=(const ToySegmentation& seg) = default;
    bool operator==(const ToySegmentation& seg) const { return m_element == seg.m_element; }

    inline Position position(const CellID& id) const {
        return Position(access()->implementation->position(id));
    }

    inline dd4hep::CellID cellID(const Position& local, const Position& global, const VolumeID& volID) const {
        return access()->implementation->cellID(local, global, volID);
    }

    inline VolumeID setVolumeID(int System, int Phi, int Theta, int Depth) const {
        return access()->implementation->setVolumeID(System, Phi, Theta, Depth);
    }

    inline CellID setCellID(int System, int Phi, int Theta, int Depth) const {
        return access()->implementation->setCellID(System, Phi, Theta, Depth);
    }

    inline int System(const CellID& aCellID) const { return access()->implementation->System(aCellID); }
    inline int Phi(const CellID& aCellID) const { return access()->implementation->Phi(aCellID); }
    inline int Theta(const CellID& aCellID) const { return access()->implementation->Theta(aCellID); }
    inline int Depth(const CellID& aCellID) const { return access()->implementation->Depth(aCellID); }

    inline int getFirst32bits(const CellID& aCellID) const { return access()->implementation->getFirst32bits(aCellID); }
    inline int getLast32bits(const CellID& aCellID) const { return access()->implementation->getLast32bits(aCellID); }

    inline CellID convertFirst32to64(const int aId32) const { return access()->implementation->convertFirst32to64(aId32); }
    inline CellID convertLast32to64(const int aId32) const { return access()->implementation->convertLast32to64(aId32); }

    inline int System(const int& aId32) const { return access()->implementation->System(aId32); }
    inline int Phi(const int& aId32) const { return access()->implementation->Phi(aId32); }
    inline int Theta(const int& aId32) const { return access()->implementation->Theta(aId32); }
    inline int Depth(const int& aId32) const { return access()->implementation->Depth(aId32); }

};

}
#endif
