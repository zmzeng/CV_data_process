function [area_of_electrode, pH, calibration_value_of_AgAgCl, ref_electrode] = get_experiment_parameters()
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here
%set experimental parameters
prompt = {'Area of the electrode in cm^2','pH','Ag/AgCl electrode potential vs. NHE'};
dlg_title = 'Set Experimental Parameters';
default_parameters = {'0.196', '7','0.2'};
input_parameters = inputdlg(prompt, dlg_title, 1, default_parameters);
roundnum = str2num(input_parameters{1});
area_of_electrode = str2num(input_parameters{1}); % in cm^2
pH = str2num(input_parameters{2});
calibration_value_of_AgAgCl = str2num(input_parameters{3});
%set ref electrode in plot
S={'Ag/AgCl','NHE','RHE'};
[Selection, ok]=listdlg('ListString',S,'SelectionMode','single','InitialValue',3,'Name','Select a reference electrode in the plot. Note that it is assumed that your ref electrode in experiment is Ag/AgCl');
ref_electrode = S{Selection};
end

