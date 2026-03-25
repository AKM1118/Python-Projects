degs_aggr = [];

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

        degs_aggr(j) = degs(2);
    end

figure;
for i = 1:3
subplot(3,1,i); hold on; grid on;
plot(degs_aggr(:,i));
plot(ones(length(degs_aggr))*et_angle(i),'r');
end