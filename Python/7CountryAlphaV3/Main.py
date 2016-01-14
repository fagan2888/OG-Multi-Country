import time
import numpy as np
import AuxiliaryClass as AUX

np.set_printoptions(threshold = 3000, linewidth=2000, suppress=True)

TimeModel=True #Activates timing the model

def Multi_Country(S,I,sigma):

    #NOTE:To run the model, simply run the Multi_Country function with your chosen levels
    #of the number of cohorts (S), the number of countries (I) and slope parameter (sigma)

    #THIS SETS ALL OF THE USER PARAMETERS

    #Country Rosters
    I_dict = {"usa":0,"eu":1,"japan":2,"china":3,"india":4,"russia":5,"korea":6} #DONT CHANGE
    I_touse = ["eu","russia","usa","japan","korea","china","india"] #CAN CHANGE

    #Parameters Zone
    g_A = 0.015 #Technical growth rate
    beta_ann=.95 #Annual discount rate
    delta_ann=.08 #Annual depreciation rate
    alpha = .3 #Capital Share of production
    chi = 1.5 #Preference for lesiure
    rho = 1.3 #Other New Parameter

    #Convergence Tolerances
    demog_ss_tol = 1e-8 #Used in getting ss for population share

    #PROGRAM LEVERS:
    #For terminal output
    PrintAges = False #Prints the different key ages in the demographics
    PrintLoc = False #Displays the current locations of the program inside key TPI functions
    PrintSSEulErrors = False #Prints the euler errors in each attempt of calculating the steady state
    PrintSS = False #Prints the result of the Steady State functions
    Print_cabqTimepaths = False #Prints the consumption, assets, and bequests timepath as it gets filled in for each iteration of TPI
    Print_HH_Eulers = False #Prints whether the equations for the household decisions are satisfied (Equations 3.22, 3.19, and sum(assets) = 0)
    CheckerMode = False #Activates not printing much of anything, used in conjunction with RobustChecker.py
    Iterate = True #Shows the current iteration number and the associated Eulers

    #For plots to display or save
    DemogGraphs = True #Activates graphing graphs with demographic data and population shares
    ShowSSGraphs = False #Activates graphs for steady-state solutions for consumption, assets, and bequests
    TPIGraphs = False #Activates showing the final graphs
    iterations_to_plot = set([]) #Which iterations of the timepath fsolve you want to plot

    #For using differing ways to solve the model
    UseDiffDemog = True #Turns on different demographics for each country
    UseSSDemog = False #Activates using only steady state demographics for TPI calculation
    UseDiffProductivities = False #Activates having e vary across cohorts
    UseTape = True #Activates setting any value of kd<0 to 0.001 in TPI calculation
    ADJUSTKOREAIMMIGRATION = True #Activates dividing Korean immigration by 100 to correctly scale with other countrys' immigration rates
    
    VectorizeHouseholdSolver = True #Activates solving the household decision equations for all agents of a single age instead of each agent seperatly

    #Adjusts the country list if we are using less than 7 Countries
    if len(I_touse) < I:
        print "WARNING: We are changing I from", I, "to", len(I_touse), "to fit the length of I_touse. So the countries we are using now are", I_touse
        I = len(I_touse)
        time.sleep(2)

    elif len(I_touse) > I:
        print "WARNING: We are changing I_touse from", I_touse, "to", I_touse[:I], "so there are", I, "regions"
        I_touse = I_touse[:I]
        time.sleep(2)

    ##INPUTS INTO THE CLASS###

    Country_Roster = (I_dict, I_touse)

    HH_params = (S,I,beta_ann,sigma)

    Firm_Params = (alpha, delta_ann, chi, rho, g_A)

    Levers = (PrintAges,PrintLoc,PrintSSEulErrors,PrintSS,ShowSSGraphs,Print_cabqTimepaths,Print_HH_Eulers,\
              CheckerMode,Iterate,TPIGraphs,UseDiffDemog,UseDiffProductivities,UseTape,\
              ADJUSTKOREAIMMIGRATION,VectorizeHouseholdSolver)


    ##WHERE THE MAGIC HAPPENS ##

    Model = AUX.OLG(Country_Roster,HH_params,Firm_Params,Levers)

    #Demographics
    Model.Demographics(demog_ss_tol, UseSSDemog=UseSSDemog)
    if DemogGraphs:
        Model.plotDemographics(T_touse="default", compare_across="T", data_year=0)

    #Steady State

    #STEADY STATE INITIAL GUESSES

    r_ss_guess = .2
    bq_ss_guess = np.ones(I)*.2
    Model.SteadyState(r_ss_guess, bq_ss_guess)

    #Timepath Iteration
    
    r_init = Model.r_ss*1.05
    bq_init = Model.bq_ss*.95
    a_init = Model.avec_ss*.7
    Model.set_initial_values(r_init, bq_init, a_init)

    Model.Timepath_fsolve(to_plot = iterations_to_plot)

    pass

#Input parameters for S, I and sigma here then execute this file to
#run the model.

start = time.time()
Multi_Country(80,7,4)
tottime=time.time()-start

if TimeModel==True:
    minutes=int(tottime/60)
    hours=int(minutes/60)
    seconds=tottime-minutes*60
    minutes=minutes-hours*60
    print "The code took:", hours, "hours,", minutes, "minutes and", seconds, "seconds to complete"

