% -------------------------------
% This file is used by opticalBatch.m to pull data from input files
% code by zmzeng12 20180310
% -------------------------------
function [time,time_fft, signal_Difference, signal_Difference_fft] = opticalDataProcess(filename)

% get basic data
datanum = length(filename);
for i=1:datanum
    dataloc = filename{i};
    A = importdata(dataloc,',',2);
    data{i} = A.data;
end
% get laser output signal 
time = data{1}(:,1);
signal_Laser = data{1}(:,2);
% get sample signal 
signal_SampleNoLaser = data{2}(:,2);
signal_SampleLaser = data{4}(:,2);
% get difference signal from two sample singal and plot it
signal_Difference = signal_SampleLaser - signal_SampleNoLaser;
% subplot(2,1,1), plot(time, signal_Difference, '.'), legend(filename);
% xlabel('Time (s)')
% ylabel('signal (V)')

% do fft
dataLength = sum(time>1.975e-6);
Y = fft(signal_Difference(dataLength:length(time)));
%plot(real(Y)), grid on;
Y2 = zeros(length(Y),1);
Y2(1:25) = Y(1:25);
signal_Difference_fft = ifft(Y2);
% subplot(2,1,2), plot(time(dataLength:length(time)), signal_Difference_fft, '.')
% hold on;
% plot(time(1:dataLength), zeros(dataLength,1), '.');
time_fft = time(dataLength:length(time));
end