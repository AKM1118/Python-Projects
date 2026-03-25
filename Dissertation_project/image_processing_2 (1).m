%% Script to find optimal calibration paramerers
% USE one picture from each angle (0, 5, 15)


degs_aggr = [];

for i = 1:5
    %change calibration parameters with fixed step
    delta_f1 = i*0;
    delta_f2 = -i*0;
    delta_c1 = +i*0;
    delta_c2 = +i*0;


    params = cameraParameters('IntrinsicMatrix',[2807.33407289217 + delta_f1,0,0;0,2841.46558202153 + delta_f2,0;3217.28666985476 + delta_c1,2780.33228321891 + delta_c2,1]);

    for j = 1:3   
               
        %read the image
        %imOrig = imread(names(j));
        imOrig = imOrig_cell{j,1};
        
        %finding checkboard (variant 1)
        im = imOrig;
        [imagePoints,boardSize] = detectCheckerboardPoints(im);
                  
        %generate world points
        squareSize = 22;
        worldPoints = generateCheckerboardPoints(boardSize, squareSize);
        
        
        %calculating extrinsics matrices
        [rotationMatrix, translationVector] = extrinsics(...
        imagePoints,worldPoints,params); %as cameraParams using your calibrationg parameters, acuired via matlab
        
        %converting matrices to pose
        [orientation, location] = extrinsicsToCameraPose(rotationMatrix, ...
        translationVector);
        
        %converting angles to Euler angles
        degs = rad2deg(rotm2eul(rotationMatrix,'zyx')); 

        degs_aggr(i,j) = degs(2);
    end

end

figure;
for i = 1:3
subplot(3,1,i); hold on; grid on;
plot(degs_aggr(:,i));
plot(ones(length(degs_aggr))*et_angle(i),'r');
end
