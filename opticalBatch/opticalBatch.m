% -------------------------------
% This file is used to read in two csv file from oscilloscope,
% and draw difference spectrum 
% with a simple filter implemented by fft
% code by zmzeng12 20180310
% -------------------------------

clc;
clear;
clear all;
addpath('D:/optical');

% get data files
[filename, pathname, filterindex] = uigetfile('*.csv', 'Pick up data. first No Laser, then Laser', 'MultiSelect','on');
cd(pathname);
figure;
hold on;

for i=1:4:length(filename)-3
    % every 4 file consists a integrated data. So process 4 files once a time
    filenameToProcess = filename(i:i+3);
    [time{i}, time_fft{i}, signal_Difference{i}, signal_Difference_fft{i}] = opticalDataProcess(filenameToProcess);
    % draw difference secptrum
    ax1 = subplot(2,1,1);
    % add filename to legend
    filename{i}=filename{i}(1:end-8);
    legendName(floor(i/4)+1) = filename(i);
    plot(time{i}, signal_Difference{i}), legend(legendName);
    xlabel(ax1, 'time (s)');
    ylabel(ax1, 'signal (V)');
    title('difference secptrum');
    % use hold all instead of hold to give figure color automaticly.
    hold all;
    % draw signal treated by FFT
    ax2 = subplot(2,1,2);
    subplot(ax2);
    plot(time_fft{i}, signal_Difference_fft{i}), legend(legendName);
    xlabel(ax2, 'time (s)');
    ylabel(ax2, 'signal_fft (V)');
    xlim([-3e-6 10e-6]);
    title('difference secptrum after FFT');
    hold all;
end

% output all data in signalDifferenceData.txt, add 20180313 by zmzeng 
f = fopen('DifferenceSpectrum.txt','w');
fprintf(f,'%s ,%s , ', legendName{:});
fprintf(f, '\n');
fprintf(f, 'time, signal');
fprintf(f, '\n');
fclose(f);

signalDifferenceData = [time{1},signal_Difference{1}];
for i=2:length(signal_Difference)
    if isempty(signal_Difference{i})
    else
        signalDifferenceData = [signalDifferenceData time{i},signal_Difference{i}];
    end
end
save('DifferenceSpectrum.txt', 'signalDifferenceData', '-append', '-ascii');

cd('D:/optical');

