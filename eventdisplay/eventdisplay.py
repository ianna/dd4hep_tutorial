from ROOT import TFile
import numpy as np
from collections import defaultdict
from math import sqrt, acos, atan2
import plotly.graph_objs as go
import plotly.colors
import re
from itertools import islice
import ROOT
ROOT.gSystem.Load("ToyCalorimeter/ToyCalorimeter")

class MCParticle():
    def __init__(self, mcp):
        self.PDG                = mcp.PDG
        self.generatorStatus    = mcp.generatorStatus
        self.simulatorStatus    = mcp.simulatorStatus
        self.charge             = mcp.charge
        self.time               = mcp.time
        self.mass               = mcp.mass
        self.vx                 = mcp.vertex.x
        self.vy                 = mcp.vertex.y
        self.vz                 = mcp.vertex.z
        self.endx               = mcp.endpoint.x
        self.endy               = mcp.endpoint.y
        self.endz               = mcp.endpoint.z
        self.px                 = mcp.momentum.x
        self.py                 = mcp.momentum.y
        self.pz                 = mcp.momentum.z
        self.endpx              = mcp.momentumAtEndpoint.x
        self.endpy              = mcp.momentumAtEndpoint.y
        self.endpz              = mcp.momentumAtEndpoint.z
        self.spin               = mcp.spin
        self.colorFlow          = mcp.colorFlow
        # self.parents
        # self.daughters
        self.energy             = sqrt(self.px*self.px +self.py*self.py +self.pz*self.pz +self.mass*self.mass)
        self.pathlength         = sqrt((self.vx-self.endx)*(self.vx-self.endx) 
                                     + (self.vy-self.endy)*(self.vy-self.endy) 
                                     + (self.vz-self.endz)*(self.vz-self.endz))

class MCCollection():
    def __init__(self, mcplist):
        self.particles           = np.array(mcplist)
        self.N                   = len(mcplist)
        self.PDG                 = np.array([mcp.PDG                 for mcp in self.particles])
        self.generatorStatus     = np.array([mcp.generatorStatus     for mcp in self.particles])
        self.simulatorStatus     = np.array([mcp.simulatorStatus     for mcp in self.particles])
        self.charge              = np.array([mcp.charge              for mcp in self.particles])
        self.time                = np.array([mcp.time                for mcp in self.particles])
        self.mass                = np.array([mcp.mass                for mcp in self.particles])
        self.vx                  = np.array([mcp.vx                  for mcp in self.particles])
        self.vy                  = np.array([mcp.vy                  for mcp in self.particles])
        self.vz                  = np.array([mcp.vz                  for mcp in self.particles])
        self.endx                = np.array([mcp.endx                for mcp in self.particles])
        self.endy                = np.array([mcp.endy                for mcp in self.particles])
        self.endz                = np.array([mcp.endz                for mcp in self.particles])
        self.px                  = np.array([mcp.px                  for mcp in self.particles])
        self.py                  = np.array([mcp.py                  for mcp in self.particles])
        self.pz                  = np.array([mcp.pz                  for mcp in self.particles])
        self.endpx               = np.array([mcp.endpx               for mcp in self.particles])
        self.endpy               = np.array([mcp.endpy               for mcp in self.particles])
        self.endpz               = np.array([mcp.endpz               for mcp in self.particles])
        self.spin                = np.array([mcp.spin                for mcp in self.particles])
        self.colorFlow           = np.array([mcp.colorFlow           for mcp in self.particles])
        self.energy              = np.array([mcp.energy              for mcp in self.particles])
    def __iter__(self):
        for mcp in self.particles:
            yield mcp

class SimTrackerHit():
    # Takes edm4hep SimTrackerHit
    def __init__(self, hit):
        self.cellID           = hit.cellID
        self.E                = hit.eDep
        self.time             = hit.time
        self.pathlength       = hit.pathLength
        self.quality          = hit.quality
        self.x                = hit.position.x
        self.y                = hit.position.y
        self.z                = hit.position.z
        self.px               = hit.momentum.x
        self.py               = hit.momentum.y
        self.pz               = hit.momentum.z
        self.r                = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        self.theta            = acos(self.z / self.r) if self.r != 0 else 0
        self.phi              = atan2(self.y, self.x)

class SimCalorimeterHit():
    # Takes edm4hep SimCalorimeterHit
    def __init__(self, hit):
        self.cellID           = hit.cellID
        self.E                = hit.energy
        self.x                = hit.position.x
        self.y                = hit.position.y
        self.z                = hit.position.z
        self.r                = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        self.theta            = acos(self.z / self.r) if self.r != 0 else 0
        self.phi              = atan2(self.y, self.x)

class SimTrackerHitCollection():
    def __init__(self, rawhits):
        self.hits             = np.array(rawhits)
        self.N                = len(rawhits)
        self.cellID           = np.array([hit.cellID                   for hit in self.hits])
        self.E                = np.array([hit.E                        for hit in self.hits])
        self.time             = np.array([hit.time                     for hit in self.hits])
        self.pathlength       = np.array([hit.pathlength               for hit in self.hits])
        self.quality          = np.array([hit.quality                  for hit in self.hits])
        self.x                = np.array([hit.x                        for hit in self.hits])
        self.y                = np.array([hit.y                        for hit in self.hits])
        self.z                = np.array([hit.z                        for hit in self.hits])
        self.px               = np.array([hit.px                       for hit in self.hits])
        self.py               = np.array([hit.py                       for hit in self.hits])
        self.pz               = np.array([hit.pz                       for hit in self.hits])
        self.r                = np.array([hit.r                        for hit in self.hits])
        self.theta            = np.array([hit.theta                    for hit in self.hits])
        self.phi              = np.array([hit.phi                      for hit in self.hits])
    def __iter__(self):
        for hit in self.hits:
            yield hit

class SimCalorimeterHitCollection():
    def __init__(self, rawhits):
        self.hits             = np.array(rawhits)
        self.N                = len(rawhits)
        self.cellID           = np.array([hit.cellID                   for hit in self.hits])
        self.E                = np.array([hit.E                        for hit in self.hits])
        self.x                = np.array([hit.x                        for hit in self.hits])
        self.y                = np.array([hit.y                        for hit in self.hits])
        self.z                = np.array([hit.z                        for hit in self.hits])
        self.r                = np.array([hit.r                        for hit in self.hits])
        self.theta            = np.array([hit.theta                    for hit in self.hits])
        self.phi              = np.array([hit.phi                      for hit in self.hits])
    def __iter__(self):
        for hit in self.hits:
            yield hit

class DetPlot():
    def __init__(self, rootfile, maxMC, subdet_collections, MC_settings):
        self.rootfile = rootfile
        self.maxMC = maxMC
        self.subdet_colls = subdet_collections
        self.collections = defaultdict(dict)
        self.pdg_vis_map = self.generate_pdg_vis_map('./PDG_IDs.txt')
        self.MC_settings = MC_settings

    def print_sizes_for_event_num(self, eventnum):
        print(f"{'Subdetector Collection':<40} {'Hits':<10}")
        print("-" * 50)
        for key, value in self.collections.items():
            if isinstance(value, dict):
                print(f"{key:<40} {value[eventnum].N:<10}")

    def getHitsForEvent(self, eventnum, branch_name):
        return self.collections[branch_name][eventnum]

    def loadHitsForEvent(self, i):
        f = TFile.Open(self.rootfile)
        events = f.Get("events")
        branch_list = events.GetListOfBranches()

        events.GetEntry(i)

        for branch in branch_list:
            branch_name = branch.GetName()

            if branch_name in self.subdet_colls.keys():
                data = getattr(events, branch_name)

                if self.subdet_colls[branch_name]['type']=='MCParticle':
                    self.collections[branch_name][i] = MCCollection([MCParticle(hit) for hit in (islice(data,self.maxMC) if self.maxMC!=-1 else data)])

                if self.subdet_colls[branch_name]['type']=='SimTrackerHit':
                    self.collections[branch_name][i] = SimTrackerHitCollection([SimTrackerHit(hit) for hit in data])

                elif self.subdet_colls[branch_name]['type']=='SimCalorimeterHit':
                    self.collections[branch_name][i] = SimCalorimeterHitCollection([SimCalorimeterHit(hit) for hit in data])

    def getHitmarkersForEvent(self, eventnum):
        hitmarkers = []
        for branch_name in self.subdet_colls.keys():
            if branch_name=="MCParticles":
                hitmarkers.extend(
                    self.plot_MC_tracks(self.collections[branch_name][eventnum])
                )
            else:
                hitmarkers.extend([
                    self.pltr_xyz(
                        self.collections[branch_name][eventnum],
                        self.subdet_colls[branch_name]['size'],
                        self.subdet_colls[branch_name]['shape'],
                        self.subdet_colls[branch_name]['color'],
                        branch_name
                    )
                ])

        return hitmarkers

    def pltr_xyz(self, hc, size, symbol, color, subdetector_name):
        if hc is None: return None
        return go.Scatter3d(
            x=hc.x,
            y=hc.y,
            z=hc.z,
            mode='markers',
            marker={'size': size, 'opacity': 1, 'symbol':symbol, 'color':color},
            text=hc.E,
            name=subdetector_name
        )

    def plot_MC_tracks(self, MCcollection):
        MCS = self.MC_settings
        mctracks = []

        sortkey = (lambda mcp: mcp.time) if MCS['sortBy']=='time' else (lambda mcp: mcp.energy)
        reverse = False if MCS['sortBy']==['time'] else True

        MCs_sorted_and_cut = sorted(MCcollection,key=sortkey,reverse=reverse)

        for mcp in MCs_sorted_and_cut:

            above_E_cutoff = mcp.energy>MCS['Ecutoff_GeV']
            above_length_cutoff = mcp.pathlength>MCS['pathlength_mm']
            
            if MCS['limitPDG']:
                show_this_particle = mcp.PDG in MCS['PDG_show']
            else:
                show_this_particle = True

            if (above_E_cutoff and above_length_cutoff and show_this_particle):

                if mcp.PDG in self.pdg_vis_map['color']:
                    color = self.pdg_vis_map['color'][mcp.PDG]
                else:
                    color = "#999999"  # Gray
                    
                lw = log(mcp.energy)+abs(log(MCS['MC_Ecutoff_GeV'])) if MCS['lineWidthByEnergy'] else MCS['defLineWidth']
                
                if mcp.PDG in self.pdg_vis_map['particle_name']:
                    particle_name = f"{self.pdg_vis_map['particle_name'][mcp.PDG]:<6s} ({mcp.energy:3.6f} GeV, {mcp.pathlength/1000:2.3f} m)"
                else:
                    particle_name = f"Unknown ({mcp.energy:3.6f} GeV, {mcp.pathlength/1000:2.3f} m)"

                mctracks.append(
                    go.Scatter3d(
                        x=[mcp.vx, mcp.endx],
                        y=[mcp.vy, mcp.endy],
                        z=[mcp.vz, mcp.endz],
                        mode='lines',
                        line=dict(color=color, width=lw),
                        text=particle_name,
                        name=particle_name
                    )
                )
        return mctracks

    def getLayout(self, plotSettings):

        xrange = plotSettings['xlim'][1] - plotSettings['xlim'][0]
        yrange = plotSettings['ylim'][1] - plotSettings['ylim'][0]
        zrange = plotSettings['zlim'][1] - plotSettings['zlim'][0]
        norm = max(xrange, yrange, zrange)

        showGrid = plotSettings['showGrid']

        layout = go.Layout(
            template        = 'none' if plotSettings['transparent'] else plotSettings['plotly_template'],
            autosize        = False,
            width           = plotSettings['width'],
            height          = plotSettings['height'],
            paper_bgcolor   = 'rgba(0,0,0,0)',
            plot_bgcolor    = 'rgba(0,0,0,0)',
            margin          = {'l': 0, 'r': 0, 'b': 0, 't': 0},
            scene           = dict(
                                xaxis = dict(nticks=4, range=plotSettings['xlim'], showgrid=showGrid, showline=showGrid, zeroline=showGrid),
                                yaxis = dict(nticks=4, range=plotSettings['ylim'], showgrid=showGrid, showline=showGrid, zeroline=showGrid),
                                zaxis = dict(nticks=4, range=plotSettings['zlim'], showgrid=showGrid, showline=showGrid, zeroline=showGrid),
                                aspectratio = dict(x=xrange/norm, y=yrange/norm, z=zrange/norm),
                                camera = dict(
                                    eye         =dict(x=0, y=1, z=0),
                                    center      =dict(x=0, y=0, z=0),
                                    up          =dict(x=0, y=1, z=0),
                                    projection  =dict(type=plotSettings['projection'])
                                ),
                            ),
            legend          = dict(
                                itemsizing = "constant",
                                itemwidth = plotSettings['itemwidth'],
                                font = dict(
                                    size = plotSettings['legend_font_size']
                                )
                            )
        )
        return layout

    def generate_pdg_vis_map(self, PDG_file):

        base_color_map = {
            "QUARKS": "#7209b7",                  # Deep purple
            "LEPTONS": "#e63946",                 # Bright red
            "GAUGE AND HIGGS BOSONS": "#ffba08",  # Bright yellow
            "DIQUARKS": "#f4a261",                # Warm orange
            "LIGHT I=1 MESONS": "#f77f00",        # Vibrant orange
            "LIGHT I=0 MESONS": "#073b4c",        # Dark teal
            "STRANGE MESONS": "#a8dadc",          # Soft blue
            "CHARMED MESONS": "#457b9d",          # Muted blue
            "BOTTOM MESONS": "#1d3557",           # Navy blue
            "CC MESONS": "#f15bb5",               # Pink
            "BB MESONS": "#ef476f",               # Coral red
            "STRANGE BARYONS": "#06d6a0",         # Bright teal
            "CHARMED BARYONS": "#118ab2",         # Medium blue
            "BOTTOM BARYONS": "#2a9d8f",  # Teal green
        }

        neg_base_color_map = {
            "QUARKS": "#7209b7",                  # Deep purple
            "LEPTONS": "#11beff",                 # Bright red
            "GAUGE AND HIGGS BOSONS": "#ffba08",  # Bright yellow
            "DIQUARKS": "#f4a261",                # Warm orange
            "LIGHT I=1 MESONS": "#f77f00",        # Vibrant orange
            "LIGHT I=0 MESONS": "#073b4c",        # Dark teal
            "STRANGE MESONS": "#a8dadc",          # Soft blue
            "CHARMED MESONS": "#457b9d",          # Muted blue
            "BOTTOM MESONS": "#1d3557",           # Navy blue
            "CC MESONS": "#f15bb5",               # Pink
            "BB MESONS": "#ef476f",               # Coral red
            "STRANGE BARYONS": "#06d6a0",         # Bright teal
            "CHARMED BARYONS": "#118ab2",         # Medium blue
            "BOTTOM BARYONS": "#2a9d8f",  # Teal green
        }

        fallback_base_color = "#999999"  # Gray

        pdg_vis_map = {
            'color': {},
            'particle_name': {}
        }

        current_category = None

        with open(PDG_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("CATEGORY"):
                    category_parts = line.split()
                    category_name = " ".join(category_parts[1:])
                    current_category = category_name
                    continue

                if not re.search(r'\d$', line):
                    continue  

                parts = line.split()
                if len(parts) < 2:
                    continue

                particle_id_int = int(parts[-1])

                particle_name = " ".join(parts[:-1]) 

                base_hex_color = base_color_map.get(current_category, fallback_base_color)

                pdg_vis_map['color'][particle_id_int] = base_hex_color
                pdg_vis_map['particle_name'][particle_id_int] = particle_name

                negative_id_int = -1*particle_id_int
                neg_base_hex_color = neg_base_color_map.get(current_category, fallback_base_color)

                pdg_vis_map['color'][negative_id_int] = neg_base_hex_color
                pdg_vis_map['particle_name'][negative_id_int] = "~" + particle_name

        return pdg_vis_map
