function sysCall_init()
    corout=coroutine.create(coroutineMain)
end

function sysCall_actuation()
    if coroutine.status(corout)~='dead' then
        local ok,errorMsg=coroutine.resume(corout)
        if errorMsg then
            error(debug.traceback(corout,errorMsg),2)
        end
    end
end

function sysCall_cleanup()
    -- do some clean-up here
end

function getHandleOfObject(objectName)
    object_handle = sim.getObjectHandle(objectName)
    return object_handle
end

function getPositionOfObject(objectName)
    object_handle = getHandleOfObject(objectName)
    object_position = sim.getObjectPosition(object_handle, -1)
    return object_position
end

function setPosition(motorName, angle)
    sim.setJointTargetPosition(motorName, angle)
end

function getTime()
    time = sim.getSimulationTime()
    return time
end


function coroutineMain()
    
    handles()

    while true do

        ----------------------------------------------------------------------------------------------
        -- Determine the error position

        ----------------------------------------------------------------------------------------------
        -- Write the equations wrt the error
        
        --Proportional
        kp_error = 0
        --Integral
        ki_error = 0
        --Derivative
        kd_error = 0
        ----------------------------------------------------------------------------------------------
        -- P + I + D equation
        torque = Kp*kp_error + Ki*ki_error + Kd*kd_error

        ----------------------------------------------------------------------------------------------
        -- Set the position of the motor according to the angle

    end

end

-- See the user manual or the available code snippets for additional callback functions and details
