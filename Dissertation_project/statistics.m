% mean_x_0 = [fitdist(experimentresults10.xAngle,'Normal').mu fitdist(experimentresults20.xAngle,'Normal').mu fitdist(experimentresults30.xAngle,'Normal').mu; fitdist(experimentresults40.xAngle,'Normal').mu fitdist(experimentresults50.xAngle,'Normal').mu fitdist(experimentresults60.xAngle,'Normal').mu; fitdist(experimentresults70.xAngle,'Normal').mu fitdist(experimentresults80.xAngle,'Normal').mu fitdist(experimentresults90.xAngle,'Normal').mu];
% mean_y_0 = [fitdist(experimentresults10.yAngle,'Normal').mu fitdist(experimentresults20.yAngle,'Normal').mu fitdist(experimentresults30.yAngle,'Normal').mu; fitdist(experimentresults40.yAngle,'Normal').mu fitdist(experimentresults50.yAngle,'Normal').mu fitdist(experimentresults60.yAngle,'Normal').mu; fitdist(experimentresults70.yAngle,'Normal').mu fitdist(experimentresults80.yAngle,'Normal').mu fitdist(experimentresults90.yAngle,'Normal').mu];
% mean_z_0 = [fitdist(experimentresults10.zAngle,'Normal').mu fitdist(experimentresults20.zAngle,'Normal').mu fitdist(experimentresults30.zAngle,'Normal').mu; fitdist(experimentresults40.zAngle,'Normal').mu fitdist(experimentresults50.zAngle,'Normal').mu fitdist(experimentresults60.zAngle,'Normal').mu; fitdist(experimentresults70.zAngle,'Normal').mu fitdist(experimentresults80.zAngle,'Normal').mu fitdist(experimentresults90.zAngle,'Normal').mu];
% 
% var_x_0 = [var(experimentresults10.xAngle) var(experimentresults20.xAngle) var(experimentresults30.xAngle); var(experimentresults40.xAngle) var(experimentresults50.xAngle) var(experimentresults60.xAngle); var(experimentresults70.xAngle) var(experimentresults80.xAngle) var(experimentresults90.xAngle)];
% var_y_0 = [var(experimentresults10.yAngle) var(experimentresults20.yAngle) var(experimentresults30.yAngle); var(experimentresults40.yAngle) var(experimentresults50.yAngle) var(experimentresults60.yAngle); var(experimentresults70.yAngle) var(experimentresults80.yAngle) var(experimentresults90.yAngle)];
% var_z_0 = [var(experimentresults10.zAngle) var(experimentresults20.zAngle) var(experimentresults30.zAngle); var(experimentresults40.zAngle) var(experimentresults50.zAngle) var(experimentresults60.zAngle); var(experimentresults70.zAngle) var(experimentresults80.zAngle) var(experimentresults90.zAngle)];
% 
% sigma_x_0 = [fitdist(experimentresults10.xAngle,'Normal').sigma fitdist(experimentresults20.xAngle,'Normal').sigma fitdist(experimentresults30.xAngle,'Normal').sigma; fitdist(experimentresults40.xAngle,'Normal').sigma fitdist(experimentresults50.xAngle,'Normal').sigma fitdist(experimentresults60.xAngle,'Normal').sigma; fitdist(experimentresults70.xAngle,'Normal').sigma fitdist(experimentresults80.xAngle,'Normal').sigma fitdist(experimentresults90.xAngle,'Normal').sigma];
% sigma_y_0 = [fitdist(experimentresults10.yAngle,'Normal').sigma fitdist(experimentresults20.yAngle,'Normal').sigma fitdist(experimentresults30.yAngle,'Normal').sigma; fitdist(experimentresults40.yAngle,'Normal').sigma fitdist(experimentresults50.yAngle,'Normal').sigma fitdist(experimentresults60.yAngle,'Normal').sigma; fitdist(experimentresults70.yAngle,'Normal').sigma fitdist(experimentresults80.yAngle,'Normal').sigma fitdist(experimentresults90.yAngle,'Normal').sigma];
% sigma_z_0 = [fitdist(experimentresults10.zAngle,'Normal').sigma fitdist(experimentresults20.zAngle,'Normal').sigma fitdist(experimentresults30.zAngle,'Normal').sigma; fitdist(experimentresults40.zAngle,'Normal').sigma fitdist(experimentresults50.zAngle,'Normal').sigma fitdist(experimentresults60.zAngle,'Normal').sigma; fitdist(experimentresults70.zAngle,'Normal').sigma fitdist(experimentresults80.zAngle,'Normal').sigma fitdist(experimentresults90.zAngle,'Normal').sigma];
% 
% 
% figure;
% t_x = tiledlayout(3,3);
% title(t_x,'xAngle 0 degrees 3m matlab image matrix')
% nexttile;
% histfit(experimentresults10.xAngle);
% nexttile;
% histfit(experimentresults20.xAngle);
% nexttile;
% histfit(experimentresults30.xAngle);
% nexttile;
% histfit(experimentresults40.xAngle);
% nexttile;
% histfit(experimentresults50.xAngle);
% nexttile;
% histfit(experimentresults60.xAngle);
% nexttile;
% histfit(experimentresults70.xAngle);
% nexttile;
% histfit(experimentresults80.xAngle);
% nexttile;
% histfit(experimentresults90.xAngle);
% 
% 
% 
% figure
% t_y = tiledlayout(3,3);
% title(t_y,'yAngle 0 degrees 3m matlab image matrix')
% nexttile;
% histfit(experimentresults10.yAngle);
% nexttile;
% histfit(experimentresults20.yAngle);
% nexttile;
% histfit(experimentresults30.yAngle);
% nexttile;
% histfit(experimentresults40.yAngle);
% nexttile;
% histfit(experimentresults50.yAngle);
% nexttile;
% histfit(experimentresults60.yAngle);
% nexttile;
% histfit(experimentresults70.yAngle);
% nexttile;
% histfit(experimentresults80.yAngle);
% nexttile;
% histfit(experimentresults90.yAngle);
% 
% 
% figure
% t_z = tiledlayout(3,3);
% title(t_z,'zAngle 0 degrees 3m matlab image matrix')
% nexttile;
% histfit(experimentresults10.zAngle);
% nexttile;
% histfit(experimentresults20.zAngle);
% nexttile;
% histfit(experimentresults30.zAngle);
% nexttile;
% histfit(experimentresults40.zAngle);
% nexttile;
% histfit(experimentresults50.zAngle);
% nexttile;
% histfit(experimentresults60.zAngle);
% nexttile;
% histfit(experimentresults70.zAngle);
% nexttile;
% histfit(experimentresults80.zAngle);
% nexttile;
% histfit(experimentresults90.zAngle);
% 
% mean_x_5 = [fitdist(experimentresults15.xAngle,'Normal').mu fitdist(experimentresults25.xAngle,'Normal').mu fitdist(experimentresults35.xAngle,'Normal').mu; fitdist(experimentresults45.xAngle,'Normal').mu fitdist(experimentresults55.xAngle,'Normal').mu fitdist(experimentresults65.xAngle,'Normal').mu; fitdist(experimentresults75.xAngle,'Normal').mu fitdist(experimentresults85.xAngle,'Normal').mu fitdist(experimentresults95.xAngle,'Normal').mu];
% mean_y_5 = [fitdist(experimentresults15.yAngle,'Normal').mu fitdist(experimentresults25.yAngle,'Normal').mu fitdist(experimentresults35.yAngle,'Normal').mu; fitdist(experimentresults45.yAngle,'Normal').mu fitdist(experimentresults55.yAngle,'Normal').mu fitdist(experimentresults65.yAngle,'Normal').mu; fitdist(experimentresults75.yAngle,'Normal').mu fitdist(experimentresults85.yAngle,'Normal').mu fitdist(experimentresults95.yAngle,'Normal').mu];
% mean_z_5 = [fitdist(experimentresults15.zAngle,'Normal').mu fitdist(experimentresults25.zAngle,'Normal').mu fitdist(experimentresults35.zAngle,'Normal').mu; fitdist(experimentresults45.zAngle,'Normal').mu fitdist(experimentresults55.zAngle,'Normal').mu fitdist(experimentresults65.zAngle,'Normal').mu; fitdist(experimentresults75.zAngle,'Normal').mu fitdist(experimentresults85.zAngle,'Normal').mu fitdist(experimentresults95.zAngle,'Normal').mu];
% 
% var_x_5 = [var(experimentresults15.xAngle) var(experimentresults25.xAngle) var(experimentresults35.xAngle); var(experimentresults45.xAngle) var(experimentresults55.xAngle) var(experimentresults65.xAngle); var(experimentresults75.xAngle) var(experimentresults85.xAngle) var(experimentresults95.xAngle)];
% var_y_5 = [var(experimentresults15.yAngle) var(experimentresults25.yAngle) var(experimentresults35.yAngle); var(experimentresults45.yAngle) var(experimentresults55.yAngle) var(experimentresults65.yAngle); var(experimentresults75.yAngle) var(experimentresults85.yAngle) var(experimentresults95.yAngle)];
% var_z_5 = [var(experimentresults15.zAngle) var(experimentresults25.zAngle) var(experimentresults35.zAngle); var(experimentresults45.zAngle) var(experimentresults55.zAngle) var(experimentresults65.zAngle); var(experimentresults75.zAngle) var(experimentresults85.zAngle) var(experimentresults95.zAngle)];
% 
% sigma_x_5 = [fitdist(experimentresults15.xAngle,'Normal').sigma fitdist(experimentresults25.xAngle,'Normal').sigma fitdist(experimentresults35.xAngle,'Normal').sigma; fitdist(experimentresults45.xAngle,'Normal').sigma fitdist(experimentresults55.xAngle,'Normal').sigma fitdist(experimentresults65.xAngle,'Normal').sigma; fitdist(experimentresults75.xAngle,'Normal').sigma fitdist(experimentresults85.xAngle,'Normal').sigma fitdist(experimentresults95.xAngle,'Normal').sigma];
% sigma_y_5 = [fitdist(experimentresults15.yAngle,'Normal').sigma fitdist(experimentresults25.yAngle,'Normal').sigma fitdist(experimentresults35.yAngle,'Normal').sigma; fitdist(experimentresults45.yAngle,'Normal').sigma fitdist(experimentresults55.yAngle,'Normal').sigma fitdist(experimentresults65.yAngle,'Normal').sigma; fitdist(experimentresults75.yAngle,'Normal').sigma fitdist(experimentresults85.yAngle,'Normal').sigma fitdist(experimentresults95.yAngle,'Normal').sigma];
% sigma_z_5 = [fitdist(experimentresults15.zAngle,'Normal').sigma fitdist(experimentresults25.zAngle,'Normal').sigma fitdist(experimentresults35.zAngle,'Normal').sigma; fitdist(experimentresults45.zAngle,'Normal').sigma fitdist(experimentresults55.zAngle,'Normal').sigma fitdist(experimentresults65.zAngle,'Normal').sigma; fitdist(experimentresults75.zAngle,'Normal').sigma fitdist(experimentresults85.zAngle,'Normal').sigma fitdist(experimentresults95.zAngle,'Normal').sigma];
% 
% 
% figure;
% t_x = tiledlayout(3,3);
% title(t_x,'xAngle 5 degrees 3m matlab image matrix')
% nexttile;
% histfit(experimentresults15.xAngle);
% nexttile;
% histfit(experimentresults25.xAngle);
% nexttile;
% histfit(experimentresults35.xAngle);
% nexttile;
% histfit(experimentresults45.xAngle);
% nexttile;
% histfit(experimentresults55.xAngle);
% nexttile;
% histfit(experimentresults65.xAngle);
% nexttile;
% histfit(experimentresults75.xAngle);
% nexttile;
% histfit(experimentresults85.xAngle);
% nexttile;
% histfit(experimentresults95.xAngle);
% 
% 
% 
% figure
% t_y = tiledlayout(3,3);
% title(t_y,'yAngle 5 degrees 3m matlab image matrix')
% nexttile;
% histfit(experimentresults15.yAngle);
% nexttile;
% histfit(experimentresults25.yAngle);
% nexttile;
% histfit(experimentresults35.yAngle);
% nexttile;
% histfit(experimentresults45.yAngle);
% nexttile;
% histfit(experimentresults55.yAngle);
% nexttile;
% histfit(experimentresults65.yAngle);
% nexttile;
% histfit(experimentresults75.yAngle);
% nexttile;
% histfit(experimentresults85.yAngle);
% nexttile;
% histfit(experimentresults95.yAngle);
% 
% 
% figure
% t_z = tiledlayout(3,3);
% title(t_z,'zAngle 5 degrees 3m matlab image matrix')
% nexttile;
% histfit(experimentresults15.zAngle);
% nexttile;
% histfit(experimentresults25.zAngle);
% nexttile;
% histfit(experimentresults35.zAngle);
% nexttile;
% histfit(experimentresults45.zAngle);
% nexttile;
% histfit(experimentresults55.zAngle);
% nexttile;
% histfit(experimentresults65.zAngle);
% nexttile;
% histfit(experimentresults75.zAngle);
% nexttile;
% histfit(experimentresults85.zAngle);
% nexttile;
% histfit(experimentresults95.zAngle);
% 
% mean_x_15 = [fitdist(experimentresults115.xAngle,'Normal').mu fitdist(experimentresults215.xAngle,'Normal').mu fitdist(experimentresults315.xAngle,'Normal').mu; fitdist(experimentresults415.xAngle,'Normal').mu fitdist(experimentresults515.xAngle,'Normal').mu fitdist(experimentresults615.xAngle,'Normal').mu; fitdist(experimentresults715.xAngle,'Normal').mu fitdist(experimentresults815.xAngle,'Normal').mu fitdist(experimentresults915.xAngle,'Normal').mu];
% mean_y_15 = [fitdist(experimentresults115.yAngle,'Normal').mu fitdist(experimentresults215.yAngle,'Normal').mu fitdist(experimentresults315.yAngle,'Normal').mu; fitdist(experimentresults415.yAngle,'Normal').mu fitdist(experimentresults515.yAngle,'Normal').mu fitdist(experimentresults615.yAngle,'Normal').mu; fitdist(experimentresults715.yAngle,'Normal').mu fitdist(experimentresults815.yAngle,'Normal').mu fitdist(experimentresults915.yAngle,'Normal').mu];
% mean_z_15 = [fitdist(experimentresults115.zAngle,'Normal').mu fitdist(experimentresults215.zAngle,'Normal').mu fitdist(experimentresults315.zAngle,'Normal').mu; fitdist(experimentresults415.zAngle,'Normal').mu fitdist(experimentresults515.zAngle,'Normal').mu fitdist(experimentresults615.zAngle,'Normal').mu; fitdist(experimentresults715.zAngle,'Normal').mu fitdist(experimentresults815.zAngle,'Normal').mu fitdist(experimentresults915.zAngle,'Normal').mu];
% 
% var_x_15 = [var(experimentresults115.xAngle) var(experimentresults215.xAngle) var(experimentresults315.xAngle); var(experimentresults415.xAngle) var(experimentresults515.xAngle) var(experimentresults615.xAngle); var(experimentresults715.xAngle) var(experimentresults815.xAngle) var(experimentresults915.xAngle)];
% var_y_15 = [var(experimentresults115.yAngle) var(experimentresults215.yAngle) var(experimentresults315.yAngle); var(experimentresults415.yAngle) var(experimentresults515.yAngle) var(experimentresults615.yAngle); var(experimentresults715.yAngle) var(experimentresults815.yAngle) var(experimentresults915.yAngle)];
% var_z_15 = [var(experimentresults115.zAngle) var(experimentresults215.zAngle) var(experimentresults315.zAngle); var(experimentresults415.zAngle) var(experimentresults515.zAngle) var(experimentresults615.zAngle); var(experimentresults715.zAngle) var(experimentresults815.zAngle) var(experimentresults915.zAngle)];
% 
% sigma_x_15 = [fitdist(experimentresults115.xAngle,'Normal').sigma fitdist(experimentresults215.xAngle,'Normal').sigma fitdist(experimentresults315.xAngle,'Normal').sigma; fitdist(experimentresults415.xAngle,'Normal').sigma fitdist(experimentresults515.xAngle,'Normal').sigma fitdist(experimentresults615.xAngle,'Normal').sigma; fitdist(experimentresults715.xAngle,'Normal').sigma fitdist(experimentresults815.xAngle,'Normal').sigma fitdist(experimentresults915.xAngle,'Normal').sigma];
% sigma_y_15 = [fitdist(experimentresults115.yAngle,'Normal').sigma fitdist(experimentresults215.yAngle,'Normal').sigma fitdist(experimentresults315.yAngle,'Normal').sigma; fitdist(experimentresults415.yAngle,'Normal').sigma fitdist(experimentresults515.yAngle,'Normal').sigma fitdist(experimentresults615.yAngle,'Normal').sigma; fitdist(experimentresults715.yAngle,'Normal').sigma fitdist(experimentresults815.yAngle,'Normal').sigma fitdist(experimentresults915.yAngle,'Normal').sigma];
% sigma_z_15 = [fitdist(experimentresults115.zAngle,'Normal').sigma fitdist(experimentresults215.zAngle,'Normal').sigma fitdist(experimentresults315.zAngle,'Normal').sigma; fitdist(experimentresults415.zAngle,'Normal').sigma fitdist(experimentresults515.zAngle,'Normal').sigma fitdist(experimentresults615.zAngle,'Normal').sigma; fitdist(experimentresults715.zAngle,'Normal').sigma fitdist(experimentresults815.zAngle,'Normal').sigma fitdist(experimentresults915.zAngle,'Normal').sigma];
% 
% 
% figure;
% t_x = tiledlayout(3,3);
% title(t_x,'xAngle 15 degrees 3m matlab image matrix')
% nexttile;
% histfit(experimentresults115.xAngle);
% nexttile;
% histfit(experimentresults215.xAngle);
% nexttile;
% histfit(experimentresults315.xAngle);
% nexttile;
% histfit(experimentresults415.xAngle);
% nexttile;
% histfit(experimentresults515.xAngle);
% nexttile;
% histfit(experimentresults615.xAngle);
% nexttile;
% histfit(experimentresults715.xAngle);
% nexttile;
% histfit(experimentresults815.xAngle);
% nexttile;
% histfit(experimentresults915.xAngle);
% 
% 
% 
% figure
% t_y = tiledlayout(3,3);
% title(t_y,'yAngle 15 degrees 3m matlab image matrix')
% nexttile;
% histfit(experimentresults115.yAngle);
% nexttile;
% histfit(experimentresults215.yAngle);
% nexttile;
% histfit(experimentresults315.yAngle);
% nexttile;
% histfit(experimentresults415.yAngle);
% nexttile;
% histfit(experimentresults515.yAngle);
% nexttile;
% histfit(experimentresults615.yAngle);
% nexttile;
% histfit(experimentresults715.yAngle);
% nexttile;
% histfit(experimentresults815.yAngle);
% nexttile;
% histfit(experimentresults915.yAngle);
% 
% 
% figure
% t_z = tiledlayout(3,3);
% title(t_z,'zAngle 15 degrees 3m matlab image matrix')
% nexttile;
% histfit(experimentresults115.zAngle);
% nexttile;
% histfit(experimentresults215.zAngle);
% nexttile;
% histfit(experimentresults315.zAngle);
% nexttile;
% histfit(experimentresults415.zAngle);
% nexttile;
% histfit(experimentresults515.zAngle);
% nexttile;
% histfit(experimentresults615.zAngle);
% nexttile;
% histfit(experimentresults715.zAngle);
% nexttile;
% histfit(experimentresults815.zAngle);
% nexttile;
% histfit(experimentresults915.zAngle);






% mean_x = [mean(experimentresults1.xAngle) mean(experimentresults2.xAngle) mean(experimentresults3.xAngle); mean(experimentresults4.xAngle) mean(experimentresults5.xAngle) mean(experimentresults6.xAngle); mean(experimentresults7.xAngle) mean(experimentresults8.xAngle) mean(experimentresults9.xAngle)];
% mean_y = [mean(experimentresults1.yAngle) mean(experimentresults2.yAngle) mean(experimentresults3.yAngle); mean(experimentresults4.yAngle) mean(experimentresults5.yAngle) mean(experimentresults6.yAngle); mean(experimentresults7.yAngle) mean(experimentresults8.yAngle) mean(experimentresults9.yAngle)];
% mean_z = [mean(experimentresults1.zAngle) mean(experimentresults2.zAngle) mean(experimentresults3.zAngle); mean(experimentresults4.zAngle) mean(experimentresults5.zAngle) mean(experimentresults6.zAngle); mean(experimentresults7.zAngle) mean(experimentresults8.zAngle) mean(experimentresults9.zAngle)];
% 
% var_x = [var(experimentresults1.xAngle) var(experimentresults2.xAngle) var(experimentresults3.xAngle); var(experimentresults4.xAngle) var(experimentresults5.xAngle) var(experimentresults6.xAngle); var(experimentresults7.xAngle) var(experimentresults8.xAngle) var(experimentresults9.xAngle)];
% var_y = [var(experimentresults1.yAngle) var(experimentresults2.yAngle) var(experimentresults3.yAngle); var(experimentresults4.yAngle) var(experimentresults5.yAngle) var(experimentresults6.yAngle); var(experimentresults7.yAngle) var(experimentresults8.yAngle) var(experimentresults9.yAngle)];
% var_z = [var(experimentresults1.zAngle) var(experimentresults2.zAngle) var(experimentresults3.zAngle); var(experimentresults4.zAngle) var(experimentresults5.zAngle) var(experimentresults6.zAngle); var(experimentresults7.zAngle) var(experimentresults8.zAngle) var(experimentresults9.zAngle)];
% 
% sigma_x = [fitdist(experimentresults1.xAngle,'Normal').sigma fitdist(experimentresults2.xAngle,'Normal').sigma fitdist(experimentresults3.xAngle,'Normal').sigma; fitdist(experimentresults4.xAngle,'Normal').sigma fitdist(experimentresults5.xAngle,'Normal').sigma fitdist(experimentresults6.xAngle,'Normal').sigma; fitdist(experimentresults7.xAngle,'Normal').sigma fitdist(experimentresults8.xAngle,'Normal').sigma fitdist(experimentresults9.xAngle,'Normal').sigma];
% sigma_y = [fitdist(experimentresults1.yAngle,'Normal').sigma fitdist(experimentresults2.yAngle,'Normal').sigma fitdist(experimentresults3.yAngle,'Normal').sigma; fitdist(experimentresults4.yAngle,'Normal').sigma fitdist(experimentresults5.yAngle,'Normal').sigma fitdist(experimentresults6.yAngle,'Normal').sigma; fitdist(experimentresults7.yAngle,'Normal').sigma fitdist(experimentresults8.yAngle,'Normal').sigma fitdist(experimentresults9.yAngle,'Normal').sigma];
% sigma_z = [fitdist(experimentresults1.zAngle,'Normal').sigma fitdist(experimentresults2.zAngle,'Normal').sigma fitdist(experimentresults3.zAngle,'Normal').sigma; fitdist(experimentresults4.zAngle,'Normal').sigma fitdist(experimentresults5.zAngle,'Normal').sigma fitdist(experimentresults6.zAngle,'Normal').sigma; fitdist(experimentresults7.zAngle,'Normal').sigma fitdist(experimentresults8.zAngle,'Normal').sigma fitdist(experimentresults9.zAngle,'Normal').sigma];
% 
% 
% figure;
% t_x = tiledlayout(3,3);
% title(t_x,'xAngle')
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
% 
% 
% 
% figure
% t_y = tiledlayout(3,3);
% title(t_y,'yAngle')
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
% 
% 
% figure
% t_z = tiledlayout(3,3);
% title(t_z,'zAngle')
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

mean_x_0 = mean(deg_0.xAngle);
mean_y_0 = mean(deg_0.yAngle);
mean_z_0 = mean(deg_0.zAngle);

var_x_0 = var(deg_0.xAngle);
var_y_0 = var(deg_0.yAngle);
var_z_0 = var(deg_0.zAngle);

sigma_x_0 = fitdist(deg_0.xAngle,'Normal').sigma;
sigma_y_0 = fitdist(deg_0.yAngle,'Normal').sigma;
sigma_z_0 = fitdist(deg_0.zAngle,'Normal').sigma;

mean_x_5 = mean(deg_5.xAngle);
mean_y_5 = mean(deg_5.yAngle);
mean_z_5 = mean(deg_5.zAngle);

var_x_5 = var(deg_5.xAngle);
var_y_5 = var(deg_5.yAngle);
var_z_5 = var(deg_5.zAngle);

sigma_x_5 = fitdist(deg_5.xAngle,'Normal').sigma;
sigma_y_5 = fitdist(deg_5.yAngle,'Normal').sigma;
sigma_z_5 = fitdist(deg_5.zAngle,'Normal').sigma;

mean_x_15 = mean(deg_15.xAngle);
mean_y_15 = mean(deg_15.yAngle);
mean_z_15 = mean(deg_15.zAngle);

var_x_15 = var(deg_15.xAngle);
var_y_15 = var(deg_15.yAngle);
var_z_15 = var(deg_15.zAngle);

sigma_x_15 = fitdist(deg_15.xAngle,'Normal').sigma;
sigma_y_15 = fitdist(deg_15.yAngle,'Normal').sigma;
sigma_z_15 = fitdist(deg_15.zAngle,'Normal').sigma;
figure;
t_x = tiledlayout(1,3);
title(t_x,'xAngle')
nexttile;
histfit(deg_0.xAngle);
nexttile;
histfit(deg_5.xAngle);
nexttile;
histfit(deg_15.xAngle);


figure;
t_y = tiledlayout(1,3);
title(t_y,'yAngle')
nexttile;
histfit(deg_0.yAngle);
nexttile;
histfit(deg_5.yAngle);
nexttile;
histfit(deg_15.yAngle);


figure;
t_z = tiledlayout(1,3);
title(t_z,'zAngle')
nexttile;
histfit(deg_0.zAngle);
nexttile;
histfit(deg_5.zAngle);
nexttile;
histfit(deg_15.zAngle);