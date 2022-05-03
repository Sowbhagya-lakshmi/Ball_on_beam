import sys
import time
import traceback
from xmlrpc import client

try:
	import sim
	
except Exception:
	print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
	print('\n[WARNING] Make sure to have following files in the directory:')
	print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')
	sys.exit()

# Global variable "client_id" for storing ID of starting the CoppeliaSim Remote connection
client_id = -1

def init_remote_api_server():

    """
    Purpose:
    ---
    This function should first close any open connections and then start
    communication thread with server i.e. CoppeliaSim.

    NOTE: In this Task, do not call the exit_remote_api_server function in case of failed connection to the server.
    The test_task_2a executable script will handle that condition.
    
    Input Arguments:
    ---
    None
    
    Returns:
    ---
    `client_id` 	:  [ integer ]
        the client_id generated from start connection remote API, it should be stored in a global variable
    
    Example call:
    ---
    client_id = init_remote_api_server()
    
    NOTE: This function will be automatically called by test_task_2a executable before starting the simulation.
    """

    global client_id

    ##############	ADD YOUR CODE HERE	##############
    
    sim.simxFinish(-1)

    client_id = sim.simxStart('127.0.0.1',19997,True,True,5000,5) #Connect to Server

    ##################################################

    return client_id

def start_simulation():#c

    """
    Purpose:
    ---
    This function should first start the simulation if the connection to server
    i.e. CoppeliaSim was successful and then wait for last command sent to arrive
    at CoppeliaSim server end.

    NOTE: In this Task, do not call the exit_remote_api_server function in case of failed connection to the server.
    The test_task_2a executable script will handle that condition.
    
    Input Arguments:
    ---
    None
    
    Returns:
    ---
    `return_code` 	:  [ integer ]
        the return code generated from the start running simulation remote API
    
    Example call:
    ---
    return_code = start_simulation()
    
    NOTE: This function will be automatically called by test_task_2a executable at the start of simulation.
    """

    global client_id

    return_code = 0

    ##############	ADD YOUR CODE HERE	##############
    
    return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)
    sim.simxGetPingTime(client_id)

    ##################################################

    return return_code

def stop_simulation():

    """
    Purpose:
    ---
    This function should stop the running simulation in CoppeliaSim server.

    NOTE: In this Task, do not call the exit_remote_api_server function in case of failed connection to the server.
    The test_task_2a executable script will handle that condition.
    
    Input Arguments:
    ---
    None
    
    Returns:
    ---
    `return_code` 	:  [ integer ]
        the return code generated from the stop running simulation remote API
    
    Example call:
    ---
    return_code = stop_simulation()
    
    NOTE: This function will be automatically called by test_task_2a executable at the end of simulation.
    """

    global client_id

    return_code = 0

    ##############	ADD YOUR CODE HERE	##############
    
    return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot)

    ##################################################

    return return_code

def exit_remote_api_server():

    """
    Purpose:
    ---
    This function should wait for the last command sent to arrive at the Coppeliasim server
    before closing the connection and then end the communication thread with server
    i.e. CoppeliaSim using simxFinish Remote API.

    Input Arguments:
    ---
    None
    
    Returns:
    ---
    None
    
    Example call:
    ---
    exit_remote_api_server()
    
    NOTE: This function will be automatically called by test_task_2a executable after ending the simulation.
    """

    global client_id

    ##############	ADD YOUR CODE HERE	##############
    
    sim.simxGetPingTime(client_id)
    sim.simxFinish(client_id)

    ##################################################

def main_func():
    return_code, revolute_joint_handle = sim.simxGetObjectHandle(client_id, "Servo_shaft", sim.simx_opmode_blocking)
    return_code, ball_handle = sim.simxGetObjectHandle(client_id, "Ball", sim.simx_opmode_blocking)
    # return_code, revolute_joint_handle = sim.simxGetObjectHandle(client_id, "Revolute_joint", sim.simx_opmode_blocking)


    # ball_pos_x = ball_pos_array[0]
    angle = 0.3

    i = 0

    curr_pos = 0
    prev_pos = 0

    setpoint = 0
    print('about to enter while')
    while i < 1000:
        # print('inside while')
        ball_pos_array =  sim.simxGetObjectPosition(client_id, ball_handle, -1, sim.simx_opmode_blocking)
        # print(ball_pos_array)
        
        curr_pos = ball_pos_array[1][0]
        kp_error = setpoint - curr_pos
        # print(curr_pos)
        Kp = -1

        kd_error = curr_pos - prev_pos
        Kd = 10

        angle = 1*(Kp*kp_error + Kd*kd_error)
        # angle = -1

        print(Kp*kp_error, Kd*kd_error)

        if angle > 1.57:
            angle = 1.57
        elif angle < -1.57:
            angle = -1.57

        # angle = -1.57

        sim.simxSetJointTargetPosition(client_id, revolute_joint_handle, angle, sim.simx_opmode_streaming)


        i += 1
        print("Angle: ",angle)
        prev_pos = curr_pos

        print('-----------------------------------------------------------')

    # time.sleep(3)
    print("Finished")

if __name__ == "__main__":
    try:
        client_id = init_remote_api_server()

        if client_id != -1:
            print("Connected successfully")

            try:
                return_code = start_simulation()
                print("Return code for starting simulation: ", return_code)

                if return_code == sim.simx_return_novalue_flag:
                    print("Simulation started correctly")
                else:
                    print("Simulation not started correctly")
                    sys.exit()
            except Exception:
                print(".............")

        else:
            print("Failed connecting to remote server")
            sys.exit()

    except Exception:
        print("Last exception")
        sys.exit()

    # time.sleep(3)
    main_func()

    # Ending the Simulation
    try:
        return_code = stop_simulation()
        
        if (return_code == sim.simx_return_novalue_flag):
            print('\nSimulation stopped correctly.')

            # Stop the Remote API connection with CoppeliaSim server
            try:
                exit_remote_api_server()

                if (start_simulation() == sim.simx_return_initialize_error_flag):
                    print('\nDisconnected successfully from Remote API Server in CoppeliaSim!')

                else:
                    print('\n[ERROR] Failed disconnecting from Remote API server!')
                    print('[ERROR] exit_remote_api_server function is not configured correctly, check the code!')

            except Exception:
                print('\n[ERROR] Your exit_remote_api_server function throwed an Exception, kindly debug your code!')
                print('Stop the CoppeliaSim simulation manually.\n')
                traceback.print_exc(file=sys.stdout)
                print()
                sys.exit()
        
        else:
            print('\n[ERROR] Failed stopping the simulation in CoppeliaSim server!')
            print('[ERROR] stop_simulation function is not configured correctly, check the code!')
            print('Stop the CoppeliaSim simulation manually.')
        
        print()
        sys.exit()

    except Exception:
        print('\n[ERROR] Your stop_simulation function throwed an Exception, kindly debug your code!')
        print('Stop the CoppeliaSim simulation manually.\n')
        traceback.print_exc(file=sys.stdout)
        print()
        sys.exit()

