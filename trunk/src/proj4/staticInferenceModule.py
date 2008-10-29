from ghostbusters import *
from util import *
import util
import random


class StaticInferenceModule:
  """
  A static inference module must compute two quantities, conditioned on provided observations:
  
    -- The posterior distribution over ghost locations.  This will be a distribution over tuples of
       where the ghosts are.  If there is only one ghost, this distribution will be over the
       (singleton tuples of) the board locations.  If there are two ghosts, this distribution will
       assign a probability to each pair of locations, and so on.  Since the ghosts are interchangeable,
       the probability for, say, ((0,1), (3,2)) will be the same as that for ((3,2), (0,1)).
       
    -- The posterior distribution over the readings at a location, given the existing readings.  Be
       careful that your computation does the right thing when the 'new' location is actually in the
       existing observations, at which point the posterior should put probability one of the known
       reading.

  This is an abstract class, which you should not modify.
  """
  
  def __init__(self, game):
    """
    Inference modules know what game they are reasoning about.
    """
    self.game = game
  
  def getGhostTupleDistributionGivenObservations(self, observations):
    """
    Compute the distribution over ghost tuples, given the evidence.
    
    Note that the observations are given as a dictionary.
    """
    ghost_tups_obs = Counter()
    ghost_tups = self.game.getInitialDistribution()
    for ghost_tup in self.game.getGhostTuples():
        p = ghost_tups.getCount(ghost_tup)
        for obs in observations.items():
            sensor, reading = obs
            Reading_given_ghost_tups = self.game.getGhostTupleDistributionGivenPreviousGhostTuple(ghost_tup, sensor)
            reading_given_ghost_tups = Reading_given_ghost_tups.getCount(reading)
            p *= reading_given_ghost_tups
        ghost_tups_obs.setCount(ghost_tup, p)
    ghost_tups_obs = normalize(ghost_tups_obs)
    return ghost_tups_obs
        
  def getReadingDistributionGivenObservations(self, observations, newLocation):
    """
    Compute the distribution over readings for the new location, given the
    current observations (given as a dictionary).
    """
    old_reading_new_loc = self.fetch(newLocation, observations)
    new_reading_obs = Counter()
    Ghost_tups_given_obs = self.getGhostTupleDistributionGivenObservations(observations)
    for ghost_tup, ghost_tups_given_obs in Ghost_tups_given_obs.items():
        Reading_given_tup = self.game.getReadingDistributionGivenGhostTuple(ghost_tup, newLocation)
        for reading in Readings.getReadings():
            reading_given_tup = Reading_given_tup.getCount(reading)
            if old_reading_new_loc != None:
                obs_given_ghost = 0.0
                if old_reading_new_loc == reading:
                    obs_given_ghost = 1.0
            new_reading_obs.incrementCount(reading, ghost_tups_given_obs * reading_given_tup)
    new_reading_given_obs = normalize(new_reading_obs)
    return new_reading_given_obs                 

class ExactStaticInferenceModule(StaticInferenceModule):
  """
  You will implement an exact inference module for the static ghostbusters game.
  
  See the abstract 'StaticInferenceModule' class for descriptions of the methods.
  
  The current implementation below is broken, returning all uniform distributions.
  """
  
  def getGhostTupleDistributionGivenObservations(self, observations):
    
    "*** YOUR CODE HERE ***"
    
    # BROKEN
    return self.game.getInitialDistribution() 




  def getReadingDistributionGivenObservations(self, observations, newLocation):
    
    "*** YOUR CODE HERE ***"
    
    # BROKEN
    return listToDistribution(Readings.getReadings())
  