function [voltage_for_plot, currentdensity, CDerror, samplename] = get_file_data(area_of_electrode, pH, calibration_value_of_AgAgCl, ref_electrode)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    [filename, pathname, ~] = uigetfile('*.txt', 'Pick all the data you want to do average for one sample','MultiSelect','on');
    cd(pathname);
    try
        for i = 1:length(filename)
            file2read = filename{1};
            data_raw{i} = read_file(file2read);
        end
        voltage_raw = data_raw{1}(:,1);
    catch
        file2read = filename;
        data_raw = read_file(file2read);
        voltage_raw = data_raw(:,1);
    end
    
    range_of_plot = set_round();
    
    voltage_for_plot = voltage_convert(ref_electrode);
    
    [currentdensity, CDerror] = voltage_average();
    
    samplename=file2read;
    
    function data_of_file = read_file(filename)
        %FIND_HEAD_LINES Summary of this function goes here
        %   Detailed explanation goes here
        fid = fopen(filename);
        line = fgetl(fid);
        nuber_of_lines = 0;
        while(isempty(regexp(line,'^[-]?[0-9]\.\d.*','match')) ~= 0)
            line = fgetl(fid);
            nuber_of_lines = 1 + nuber_of_lines;
        end
        fclose(fid);
        if(nuber_of_lines ~= 0)
            fdata = importdata(filename,',',nuber_of_lines-1);
            data_of_file = fdata.data;
        else
            fdata = importdata(filename,',');
            data_of_file = fdata;
        end
        
    end

    function [range] = set_round()
        %set the round
        Nummax=(find(voltage_raw==max(voltage_raw)))';
        Nummin=(find(voltage_raw==min(voltage_raw)))';
        Turnpoint=sort([Nummax Nummin]);
        Numround=length(Turnpoint);
        prompt=strcat('There are ',num2str(Numround),' rounds of scans in CV (the forward and backward scans are considered as two rounds). Which round of the CV curve do you want to plot? ');
        dlg_title='Input';
        num_lines=1;
        default_value={'1'};
        answer=inputdlg(prompt,dlg_title,num_lines,default_value);
        roundnum= str2num(answer{1});
        if roundnum<Numround
            range=Turnpoint(roundnum):Turnpoint(roundnum+1)-1;
        elseif roundnum==Numround
            range=Turnpoint(end):length(voltage_raw);
        else
            range=1:length(voltage_raw);
        end
    end

    function [voltage_for_plot] = voltage_convert(ref_electrode)
        voltage_for_plot = voltage_raw(range_of_plot);
        if strcmp(ref_electrode, 'NHE')
            voltage_for_plot = voltage_for_plot + calibration_value_of_AgAgCl;
        elseif strcmp(ref_electrode, 'RHE')
            voltage_for_plot = voltage_for_plot + calibration_value_of_AgAgCl + 0.059 * pH;
        end
    end

    function [currentdensity, CDerror] = voltage_average()
        try
            current_for_plot = zeros(length(filename), length(range_of_plot));
            for i=1:length(filename)
                data = data_raw{i};
                current_for_plot(i,:)=(data(range_of_plot,2))';
            end
            dataave=mean(current_for_plot,1);
            dataerror=std(current_for_plot,1,1);
            CDerror=1000*dataerror/area_of_electrode;
            CDerror=CDerror';
            currentdensity=1000*dataave/area_of_electrode;
            currentdensity=currentdensity';
        catch
            dataave=data_raw(range_of_plot,2);
            CDerror = zeros(length(range_of_plot),1);
            currentdensity=1000*dataave/area_of_electrode;
        end
    end
end

