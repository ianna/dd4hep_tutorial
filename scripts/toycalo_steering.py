from DDSim.DD4hepSimulation import DD4hepSimulation
from g4units import mm, GeV, MeV, keV, eV
from math import pi, atan2

# Sets up the Cerenkov and scintillation physics
def setupCerenkovScint(kernel):
     from DDG4 import PhysicsList
     seq = kernel.physicsList()

     scint = PhysicsList(kernel, 'Geant4ScintillationPhysics/ScintillationPhys')
     scint.VerboseLevel = 0
     scint.TrackSecondariesFirst = True
     scint.enableUI()
     seq.adopt(scint)

     cerenkov = PhysicsList(kernel, 'Geant4CerenkovPhysics/CerenkovPhys')
     cerenkov.VerboseLevel = 0
     cerenkov.MaxNumPhotonsPerStep = 10
     cerenkov.MaxBetaChangePerStep = 10.0
     cerenkov.TrackSecondariesFirst = True
     cerenkov.enableUI()
     seq.adopt(cerenkov)

     ph = PhysicsList(kernel, 'Geant4OpticalPhotonPhysics/OpticalGammaPhys')
     ph.addParticleConstructor('G4OpticalPhoton')
     ph.VerboseLevel = 0
     ph.enableUI()
     seq.adopt(ph)

     return None

# Sets up a custom EDM4hep output for the ToyCalorimeter if using custom readout
def setupEDM4hepOutputToyCalo(dd4hepSimulation):
     from DDG4 import EventAction, Kernel
     dd = dd4hepSimulation
     evt_edm4hep = EventAction(Kernel(),'Geant4EDM4ToyReadout/'+dd.outputFile,True)
     evt_edm4hep.Control = True
     output = dd.outputFile
     if not dd.outputFile.endswith(dd.outputConfig.myExtension):
          output = dd.outputFile + dd.outputConfig.myExtension
     evt_edm4hep.Output = output
     evt_edm4hep.enableUI()
     Kernel().eventAction().add(evt_edm4hep)
     eventPars = dd.meta.parseEventParameters()
     evt_edm4hep.RunHeader = dd.meta.addParametersToRunHeader(dd)
     evt_edm4hep.EventParametersString, evt_edm4hep.EventParametersInt, evt_edm4hep.EventParametersFloat = eventPars
     evt_edm4hep.RunNumberOffset = dd.meta.runNumberOffset if dd.meta.runNumberOffset > 0 else 0
     evt_edm4hep.EventNumberOffset = dd.meta.eventNumberOffset if dd.meta.eventNumberOffset > 0 else 0
     return None

# See DD4hep/DDG4/python/DDSim/DD4hepSimulation.py
SIM = DD4hepSimulation()
SIM.runType = "batch"

# (1) VERBOSE, DEBUG, INFO, WARNING, ERROR, FATAL, ALWAYS (7)
SIM.printLevel = 3
SIM.output.geometry = 2
SIM.output.inputStage = 3
SIM.output.kernel = 3
SIM.output.part = 3
SIM.output.random = 6

# Convenience dict to gather commonly used settings
settings = {
     'opticalPhysics': setupCerenkovScint,
     'edep' : 1*keV,
     'N'        : 5,
     'particle' : 'e-',
     'momentum' : 10*GeV,
     'plusminus': 0.05*10*GeV,
     'theta'    : [90*pi/180.0, 90*pi/180.0],
     'phi'      : [(0)*pi/180.0, (360)*pi/180.0],
     'compactFile': '../compact/ToyCalorimeter.xml',
}

#~~~~~~~~~~~~~~ Settings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SIM.compactFile = settings['compactFile']
SIM.numberOfEvents = settings['N']
SIM.skipNEvents = 0
SIM.outputFile ="toy_calorimeter_output.root"

# If using a custom hit class
# SIM.outputConfig.userOutputPlugin = setupEDM4hepOutputToyCalo
# SIM.outputConfig.myExtension      = '.root'

#~~~~~~~~~~~~~~ Particle Gun ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SIM.enableGun        = True
SIM.gun.multiplicity = 1
SIM.gun.distribution = 'uniform'
SIM.gun.particle     = settings['particle']
SIM.gun.position     = (0, 0, 0)
SIM.gun.momentumMin  = settings['momentum']-settings['plusminus']
SIM.gun.momentumMax  = settings['momentum']+settings['plusminus']
SIM.gun.phiMin       = settings['phi'][0]
SIM.gun.phiMax       = settings['phi'][1]
SIM.gun.thetaMin     = settings['theta'][0]
SIM.gun.thetaMax     = settings['theta'][1]

#~~~~~~~~~~~~~~ Sensitive action filter cuts ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SIM.filter.filters = {
     'edep':    {'name':     'EnergyDepositMinimumCut/edep',
                 'parameter':{'Cut':settings['edep']}},
}

#~~~~~~~~~~~~~~ Calorimeter ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SIM.action.calorimeterSDTypes = ['calorimeter'] # same as sensitive type in compact XML
SIM.filter.mapDetFilter['MyToyCalorimeter']   = 'edep'

# If using a custom sensitive action
# SIM.action.mapActions["MyToyCalorimeter"]     = "ToyCalorimeter_SDAction"

# If using a custom hit class
# SIM.action.mapActions["MyToyCalorimeter"]     = "ToyCalorimeter_SDAction_Custom"

#~~~~~~~~~~~~~~ MC Particle handling ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SIM.part.keepAllParticles                  = False
SIM.part.minimalKineticEnergy              = 100*MeV
SIM.part.minDistToParentVertex             = 2.2e-14
SIM.part.enableDetailedHitsAndParticleInfo = False
SIM.part.printEndTracking                  = False
SIM.part.printStartTracking                = False
SIM.part.saveProcesses                     = ['Decay']
SIM.part.userParticleHandler               = ''

#~~~~~~~~~~~~~~ Physics ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SIM.physics.decays     = False
SIM.physics.list       = "FTFP_BERT"
SIM.physics.pdgfile    = None
SIM.physics.rangecut   = None
SIM.physics.rejectPDGs = {1, 2, 3, 4, 5, 6,
                          3201, 3203, 4101, 4103,
                          21, 23, 24, 25, 
                          5401, 2203, 5403,
                          3101, 3103, 4403,
                          2101, 5301, 2103, 5303,
                          4301, 1103, 4303, 5201, 
                          5203, 3303, 4201, 4203, 
                          5101, 5103, 5503}
SIM.physics.zeroTimePDGs = {17, 11, 13, 15}
SIM.physics.setupUserPhysics(settings['opticalPhysics'])

#~~~~~~~~~~~~~~ Random Generator ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SIM.random.enableEventSeed = False
SIM.random.file            = None
SIM.random.luxury          = 1
SIM.random.replace_gRandom = True
SIM.random.seed            = None
SIM.random.type            = None