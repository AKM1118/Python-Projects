mean_x = [mean(experimentresults1.xAngle) mean(experimentresults2.xAngle) mean(experimentresults3.xAngle); mean(experimentresults4.xAngle) mean(experimentresults5.xAngle) mean(experimentresults6.xAngle); mean(experimentresults7.xAngle) mean(experimentresults8.xAngle) mean(experimentresults9.xAngle)];
mean_y = [mean(experimentresults1.yAngle) mean(experimentresults2.yAngle) mean(experimentresults3.yAngle); mean(experimentresults4.yAngle) mean(experimentresults5.yAngle) mean(experimentresults6.yAngle); mean(experimentresults7.yAngle) mean(experimentresults8.yAngle) mean(experimentresults9.yAngle)];
mean_z = [mean(experimentresults1.zAngle) mean(experimentresults2.zAngle) mean(experimentresults3.zAngle); mean(experimentresults4.zAngle) mean(experimentresults5.zAngle) mean(experimentresults6.zAngle); mean(experimentresults7.zAngle) mean(experimentresults8.zAngle) mean(experimentresults9.zAngle)];

var_x = [var(experimentresults1.xAngle) var(experimentresults2.xAngle) var(experimentresults3.xAngle); var(experimentresults4.xAngle) var(experimentresults5.xAngle) var(experimentresults6.xAngle); var(experimentresults7.xAngle) var(experimentresults8.xAngle) var(experimentresults9.xAngle)];
var_y = [var(experimentresults1.yAngle) var(experimentresults2.yAngle) var(experimentresults3.yAngle); var(experimentresults4.yAngle) var(experimentresults5.yAngle) var(experimentresults6.yAngle); var(experimentresults7.yAngle) var(experimentresults8.yAngle) var(experimentresults9.yAngle)];
var_z = [var(experimentresults1.zAngle) var(experimentresults2.zAngle) var(experimentresults3.zAngle); var(experimentresults4.zAngle) var(experimentresults5.zAngle) var(experimentresults6.zAngle); var(experimentresults7.zAngle) var(experimentresults8.zAngle) var(experimentresults9.zAngle)];

sigma_x = [fitdist(experimentresults1.xAngle,'Normal').sigma fitdist(experimentresults2.xAngle,'Normal').sigma fitdist(experimentresults3.xAngle,'Normal').sigma; fitdist(experimentresults4.xAngle,'Normal').sigma fitdist(experimentresults5.xAngle,'Normal').sigma fitdist(experimentresults6.xAngle,'Normal').sigma; fitdist(experimentresults7.xAngle,'Normal').sigma fitdist(experimentresults8.xAngle,'Normal').sigma fitdist(experimentresults9.xAngle,'Normal').sigma];
sigma_y = [fitdist(experimentresults1.yAngle,'Normal').sigma fitdist(experimentresults2.yAngle,'Normal').sigma fitdist(experimentresults3.yAngle,'Normal').sigma; fitdist(experimentresults4.yAngle,'Normal').sigma fitdist(experimentresults5.yAngle,'Normal').sigma fitdist(experimentresults6.yAngle,'Normal').sigma; fitdist(experimentresults7.yAngle,'Normal').sigma fitdist(experimentresults8.yAngle,'Normal').sigma fitdist(experimentresults9.yAngle,'Normal').sigma];
sigma_z = [fitdist(experimentresults1.zAngle,'Normal').sigma fitdist(experimentresults2.zAngle,'Normal').sigma fitdist(experimentresults3.zAngle,'Normal').sigma; fitdist(experimentresults4.zAngle,'Normal').sigma fitdist(experimentresults5.zAngle,'Normal').sigma fitdist(experimentresults6.zAngle,'Normal').sigma; fitdist(experimentresults7.zAngle,'Normal').sigma fitdist(experimentresults8.zAngle,'Normal').sigma fitdist(experimentresults9.zAngle,'Normal').sigma];


figure;
t_x = tiledlayout(3,3);
title(t_x,'xAngle')
nexttile;
histfit(experimentresults1.xAngle);
nexttile;
histfit(experimentresults2.xAngle);
nexttile;
histfit(experimentresults3.xAngle);
nexttile;
histfit(experimentresults4.xAngle);
nexttile;
histfit(experimentresults5.xAngle);
nexttile;
histfit(experimentresults6.xAngle);
nexttile;
histfit(experimentresults7.xAngle);
nexttile;
histfit(experimentresults8.xAngle);
nexttile;
histfit(experimentresults9.xAngle);



figure
t_y = tiledlayout(3,3);
title(t_y,'yAngle')
nexttile;
histfit(experimentresults1.yAngle);
nexttile;
histfit(experimentresults2.yAngle);
nexttile;
histfit(experimentresults3.yAngle);
nexttile;
histfit(experimentresults4.yAngle);
nexttile;
histfit(experimentresults5.yAngle);
nexttile;
histfit(experimentresults6.yAngle);
nexttile;
histfit(experimentresults7.yAngle);
nexttile;
histfit(experimentresults8.yAngle);
nexttile;
histfit(experimentresults9.yAngle);


figure
t_z = tiledlayout(3,3);
title(t_z,'zAngle')
nexttile;
histfit(experimentresults1.zAngle);
nexttile;
histfit(experimentresults2.zAngle);
nexttile;
histfit(experimentresults3.zAngle);
nexttile;
histfit(experimentresults4.zAngle);
nexttile;
histfit(experimentresults5.zAngle);
nexttile;
histfit(experimentresults6.zAngle);
nexttile;
histfit(experimentresults7.zAngle);
nexttile;
histfit(experimentresults8.zAngle);
nexttile;
histfit(experimentresults9.zAngle);

% figure
% t_x = tiledlayout(3,3);
% title(t_x,'xAngle');
% nexttile;
% histfit(experimentresults1.xAngle);
% nexttile;
% histfit(experimentresults2.xAngle);
% nexttile;
% histfit(experimentresults3.xAngle);
% nexttile;
% histfit(experimentresults4.xAngle);
% nexttile;
% histfit(experimentresults5.xAngle);
% nexttile;
% histfit(experimentresults6.xAngle);
% nexttile;
% histfit(experimentresults7.xAngle);
% nexttile;
% histfit(experimentresults8.xAngle);
% nexttile;
% histfit(experimentresults9.xAngle);


% figure
% t_y = tiledlayout(3,3);
% title(t_y,'yAngle');
% nexttile;
% histfit(experimentresults1.yAngle);
% nexttile;
% histfit(experimentresults2.yAngle);
% nexttile;
% histfit(experimentresults3.yAngle);
% nexttile;
% histfit(experimentresults4.yAngle);
% nexttile;
% histfit(experimentresults5.yAngle);
% nexttile;
% histfit(experimentresults6.yAngle);
% nexttile;
% histfit(experimentresults7.yAngle);
% nexttile;
% histfit(experimentresults8.yAngle);
% nexttile;
% histfit(experimentresults9.yAngle);


% figure
% t_z = tiledlayout(3,3);
% title(t_z,'zAngle');
% nexttile;
% histfit(experimentresults1.zAngle);
% nexttile;
% histfit(experimentresults2.zAngle);
% nexttile;
% histfit(experimentresults3.zAngle);
% nexttile;
% histfit(experimentresults4.zAngle);
% nexttile;
% histfit(experimentresults5.zAngle);
% nexttile;
% histfit(experimentresults6.zAngle);
% nexttile;
% histfit(experimentresults7.zAngle);
% nexttile;
% histfit(experimentresults8.zAngle);
% nexttile;
% histfit(experimentresults9.zAngle);