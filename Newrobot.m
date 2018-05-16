classdef Newrobot < handle
    %NEWROBOT Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
    Connection
    Light
    DistSensor
    MotorLeft
    MotorRight
    Motors
    BgLeftSensor
    BgRightSensor
    BgLeft
    BgRight
    ObstacleDistance
    Srfc_threshold = 5
    Field
    Power = 40
    OutDist = 70
    TurnSpeed = 15
    ReverseSpeed = -10
    Parking = false
    end
    
    methods
    function obj = Newrobot(h, light, dist, mleft, mright, bgleft, bgright, motors)
            obj.Connection = h;
            obj.Light = light;
            obj.DistSensor = dist;
            obj.MotorLeft = NXTMotor(mleft);
            obj.MotorRight = NXTMotor(mright);
            obj.Motors = NXTMotor(motors);
            obj.BgLeftSensor = bgleft;
            obj.BgRightSensor = bgright;
            
            OpenUltrasonic(obj.DistSensor);
            OpenLight(obj.BgLeftSensor, 'ACTIVE');
            OpenLight(obj.BgRightSensor, 'ACTIVE');
            obj.updateDistance();
            obj.updateBG();
        end
        function lightON(obj)
            SwitchLamp(obj.Light, 'on');
        end
        function lightOFF(obj)
            SwitchLamp(obj.Light, 'off');
        end
        function obj = update(obj, i)
            obj.updateDistance();
            obj.updateField(i);
        end
        function obj = updateDistance(obj)
            obj.ObstacleDistance = GetUltrasonic(obj.DistSensor);
        end
        function obj = updateBG(obj)
            obj.BgLeft = GetLight(obj.BgLeftSensor);
            obj.BgRight = GetLight(obj.BgRightSensor);
        end
        function obj = updateField(obj, i)
            surface = max(obj.BgLeft, obj.BgRight);
            obj.updateBG();
            if mod(i, 5) == 0
                new_surface = max(obj.BgLeft, obj.BgRight);
                if new_surface - surface <= obj.Srfc_threshold
                    if new_surface > 540
                        if ~strcmp(obj.Field, 'White')
                            disp('Changed to White');
                            disp(new_surface)
                            obj.Power = 20;
                            obj.lightOFF();
                            obj.runMotors();
                        end
                        obj.Field = 'White';
                    elseif new_surface > 440

                        if ~strcmp(obj.Field, 'Gray')
                            disp('Changed to Gray');
                            disp(new_surface)
                            obj.Power = 15;
                            obj.lightON();
                            obj.runMotors();
                        end
                        obj.Field = 'Gray';

                    else
                        if ~strcmp(obj.Field, 'Green')
                            disp('Changed to Green');
                            disp(new_surface)
                            obj.Power = 35;
                            obj.lightOFF();
                            obj.runMotors();
                        end
                        obj.Field = 'Green';
                    end
                end
            end
        end
        function obj = outOfWay(obj)
            diff = abs(obj.BgLeft - obj.BgRight);
            if diff > obj.OutDist
                if obj.BgLeft > obj.BgRight
                    obj.turnRight();
                else
                    obj.turnLeft();
                end
            end
        end
        function obj = turnRight(obj)
            obj.MotorRight.Stop('brake');
            obj.rightSpeed(obj.ReverseSpeed);
            obj.leftSpeed(obj.TurnSpeed);
            while abs(obj.BgLeft - obj.BgRight) > obj.OutDist
                obj.updateBG();
            end
            obj.runMotors();
        end
        function obj = turnLeft(obj)
            obj.MotorLeft.Stop('brake');
            obj.leftSpeed(obj.ReverseSpeed);
            obj.rightSpeed(obj.TurnSpeed);
            while abs(obj.BgLeft - obj.BgRight) > obj.OutDist
                obj.updateBG();
            end
            obj.runMotors();
        end
        function leftSpeed(obj, value)
            if strcmp(obj.Field, 'Gray')
                %value = -5;
                disp('Grey Crash LEFT');
                disp(value);
            end
            obj.MotorLeft.Power = value;
            obj.MotorLeft.SendToNXT();
        end
        function rightSpeed(obj, value)
            if strcmp(obj.Field, 'Gray')
                %value = -5;
                disp('Grey Crash Right');
                disp(value);
            end
            obj.MotorRight.Power = value;
            obj.MotorRight.SendToNXT();
        end
        function runMotors(obj)
            obj.MotorLeft.Power = obj.Power;
            obj.MotorRight.Power = obj.Power;
            obj.MotorLeft.SendToNXT();
            obj.MotorRight.SendToNXT();
        end
        function stopMotors(obj)
            obj.Motors.Stop('brake')
        end
        function canPark(obj)
            if obj.BgLeft < 370 && obj.BgRight < 370
                obj.Parking = true;
                obj.stopMotors();
            end
        end
        function checkObstacle(obj)
            if obj.ObstacleDistance < 10
                obj.stopMotors();
            else
                obj.runMotors();
            end
        end
        function drive(obj)
            i = 0;
            while ~obj.Parking
                obj.update(i);
                obj.outOfWay();
                i = i + 1;
                obj.checkObstacle();
                obj.canPark();
                %disp(obj.ObstacleDistance);
            end
            disp('Parking Time!');
            obj.MotorLeft.TachoLimit = 150;
            obj.leftSpeed(20);
            pause(2);
            obj.updateDistance();
            if obj.ObstacleDistance < 20
                disp('Right taken')
                obj.MotorRight.TachoLimit = 100;
                obj.MotorLeft.TachoLimit = 100;
                obj.rightSpeed(-20);
                obj.leftSpeed(-20);
                pause(3);
                obj.MotorRight.TachoLimit = 200;
                obj.rightSpeed(20);
                pause(3);
            end
            obj.MotorLeft.TachoLimit = 0;
            obj.MotorRight.TachoLimit = 0;
            obj.Power = 10;
            obj.Field = 'White';
            while strcmp(obj.Field,'White')
                obj.runMotors();
                obj.update(0);
                obj.outOfWay();
            end
            obj.stopMotors();
            disp('Parked');
            obj.lightOFF();
        end
    end
end

