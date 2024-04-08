function result = angle_deg(varargin)

im = varargin{1};
cameraParams = evalin("base","cameraParams");
if nargin == 2
    % Obtain information about the input image source
    info = varargin{2};
end
[imagePoints,boardSize] = detectCheckerboardPoints(im);

squareSize = 22;
worldPoints = generateCheckerboardPoints(boardSize, squareSize);
im = insertMarker(im, imagePoints, 'x', 'Color', 'red', 'Size', 5);

%calculating extrinsics matrices
[rotationMatrix, translationVector] = extrinsics(...
imagePoints,worldPoints,cameraParams); %as cameraParams using your calibrationg parameters, acuired via matlab

%converting matrices to pose
%[orientation, location] = extrinsicsToCameraPose(rotationMatrix, ...
%translationVector);
%test = imagePoints(71);
%converting angles to Euler angles
disp('Measured angles:')
deg = rad2deg(rotm2eul(rotationMatrix,'zyx'));
disp(deg);
zAng = deg(1);
xAng = deg(2);
yAng = deg(3);
deg_val = [xAng yAng zAng];
result.im_points = im;
result.deg_val = deg_val;
result.zAng = zAng;
result.yAng = yAng;
result.xAng = xAng;
end

