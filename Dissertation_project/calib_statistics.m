t_x = tiledlayout(2,2);
title(t_x,'xAngle value for different calibration params');

% nexttile;
% plot(paramexperimentfx10.param10,paramexperimentfx10.xAngle,paramexperimentfx10.param10,paramexperimentfx11.xAngle,paramexperimentfx10.param10,paramexperimentfx12.xAngle);
% title('fx on 1 Matrix')
% grid on
% xlabel('fx')
% ylabel('degrees')
% legend('0 degrees','15 degrees','5 degrees')
% nexttile;
% plot(paramexperimentfy10.param10,paramexperimentfy10.xAngle,paramexperimentfy10.param10,paramexperimentfy11.xAngle,paramexperimentfy10.param10,paramexperimentfy12.xAngle);
% title('fy on 1 Matrix')
% grid on
% xlabel('fy')
% ylabel('degrees')
% legend('0 degrees','15 degrees','5 degrees')
% nexttile;
% plot(paramexperimentcx10.param10,paramexperimentcx10.xAngle,paramexperimentcx10.param10,paramexperimentcx11.xAngle,paramexperimentcx10.param10,paramexperimentcx12.xAngle);
% title('cx on 1 Matrix')
% grid on
% xlabel('cx')
% ylabel('degrees')
% legend('0 degrees','15 degrees','5 degrees')
% nexttile;
% plot(paramexperimentcy10.param10,paramexperimentcy10.xAngle,paramexperimentcy10.param10,paramexperimentcy11.xAngle,paramexperimentcy10.param10,paramexperimentcy12.xAngle);
% title('cy on 1 Matrix')
% grid on
% xlabel('cy')
% ylabel('degrees')
% legend('0 degrees','15 degrees','5 degrees')

nexttile;
plot(paramexperimentfx20.param20,paramexperimentfx20.xAngle,paramexperimentfx20.param20,paramexperimentfx21.xAngle,paramexperimentfx20.param20,paramexperimentfx22.xAngle);
title('fx on normal Matrix')
grid on
xlabel('fx')
ylabel('degrees')
legend('0 degrees','15 degrees','5 degrees')
nexttile;
plot(paramexperimentfy20.param20,paramexperimentfy20.xAngle,paramexperimentfy20.param20,paramexperimentfy21.xAngle,paramexperimentfy20.param20,paramexperimentfy22.xAngle);
title('fy on normal Matrix')
grid on
xlabel('fy')
ylabel('degrees')
legend('0 degrees','15 degrees','5 degrees')
nexttile;
plot(paramexperimentcx20.param20,paramexperimentcx20.xAngle,paramexperimentcx20.param20,paramexperimentcx21.xAngle,paramexperimentcx20.param20,paramexperimentcx22.xAngle);
title('cx on normal Matrix')
grid on
xlabel('cx')
ylabel('degrees')
legend('0 degrees','15 degrees','5 degrees')
nexttile;
plot(paramexperimentcy20.param20,paramexperimentcy20.xAngle,paramexperimentcy20.param20,paramexperimentcy21.xAngle,paramexperimentcy20.param20,paramexperimentcy22.xAngle);
title('cy on normal Matrix')
grid on
xlabel('cy')
ylabel('degrees')
legend('0 degrees','15 degrees','5 degrees')