clear;

%get parameters
[area_of_electrode, pH, calibration_value_of_AgAgCl, ref_electrode] = get_experiment_parameters;

%prepare the figure
figure;
hold on;
xlabel(strcat('voltage (V) vs.', ref_electrode));
ylabel('current density (mA/cm2)')

%load one dataset

[voltage_for_plot, currentdensity, CDerror, samplename] = get_file_data(area_of_electrode, pH, calibration_value_of_AgAgCl, ref_electrode);
errorbar(voltage_for_plot,currentdensity,CDerror,'Color',[rand() rand() rand()]);
number_of_data = 1;
legend2save={};
legend2save{end+1}=samplename;
data2save=[voltage_for_plot currentdensity CDerror];
choice=questdlg('Add another dataset to the plot?', ...
    'Add Data', ...
    'Yes','No','No');
while strcmp(choice,'Yes')
    [voltage_for_plot, currentdensity, CDerror, samplename] = get_file_data(area_of_electrode, pH, calibration_value_of_AgAgCl, ref_electrode);
    errorbar(voltage_for_plot,currentdensity,CDerror,'Color',[rand() rand() rand()]);
    number_of_data = number_of_data + 1;
    legend2save{end+1}=samplename;
    data2save=[voltage_for_plot currentdensity CDerror];
    data2save=[data2save voltage_for_plot currentdensity CDerror];
    choice=questdlg('Add another dataset to the plot?', ...
    'Add Data', ...
    'Yes','No','No');
end

legend(legend2save);
hold off;
save('CVscan.txt','data2save','-ASCII');