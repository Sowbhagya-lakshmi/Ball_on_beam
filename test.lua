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

function handles()
    revolute_joint_handle = sim.getObjectHandle("Servo_shaft")
    ball_handle = sim.getObjectHandle( "Ball")
end

function coroutineMain()
    handles()

    angle = 0.3
    
    i = 0
    
    curr_pos = 0
    prev_pos = 0

    setpoint = 0

    while true do
        ball_pos_array = sim.getObjectPosition(ball_handle, -1)
        curr_pos = ball_pos_array[1]
        kp_error = setpoint - curr_pos

        Kp = -1

        kd_error = curr_pos - prev_pos
        Kd = 20

        angle = 1*(Kp*kp_error + Kd*kd_error)

        if angle > 1.57 then
            angle = 1.57
        elseif angle < -1.57 then
            angle = -1.57
        end


        sim.setJointTargetPosition(revolute_joint_handle, angle)

        i = i + 1
        
        prev_pos = curr_pos

    end

end

-- See the user manual or the available code snippets for additional callback functions and details
