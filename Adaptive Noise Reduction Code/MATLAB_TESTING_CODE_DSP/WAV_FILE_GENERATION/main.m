close all
clc
clear all
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%INIT FILE OUTPUTS
input_num = 1;
output_num = 1;
loading = '';
w = warning('query','last')
id = w.identifier;
warning('off',id)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%READ WAV FILE
for idx = 1:91
    clearvars -except idx input_num output_num loading w id
    input_filename = 'INPUT_AUDIO\'+string(input_num)+'.wav'
    [signal,Fs] = audioread(input_filename);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %ADD NOISE
    for(j=1:15)
        if j==1
            SNR = 50;
        elseif j ==2
            SNR = 45;
        elseif j ==3
            SNR = 40;
        elseif j ==4
            SNR = 35;
        elseif j == 5
            SNR = 30;
        elseif j == 6
            SNR = 25;
        elseif j == 7
            SNR = 20;
        elseif j == 8
            SNR = 15;
        elseif j == 9
            SNR = 10;
        elseif j == 10
            SNR = 5;
        elseif j == 11
            SNR = 0;
        elseif j == 12
            SNR = -5;
        elseif j == 13
            SNR = -10;
        elseif j == 14
            SNR = -15;
        elseif j == 15
            SNR = 55;
        end
    
        noise = randn(size(signal))*std(signal)/db2mag(SNR);
    
        noisy_signal = signal + noise;
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %WRITE OUTPUT WAV FILE
        output_filename = "OUTPUT_AUDIO\"+string(idx)+"_"+string(SNR)+'.wav';
        output_num = output_num + 1;
        
        audiowrite(output_filename,noisy_signal,Fs);

        figure(1)
        t1 = 0:1/Fs:(length(noisy_signal)-1)/Fs;
        plot(t1,noisy_signal)
        hold on
        title_str = "NOISE OUTPUT: " + string(idx);
        title(title_str)
        xlabel("Time [S]")
        ylabel("Amplitude [Au]")
        hold off
    end
    input_num = input_num + 1;
    clc
    display("                                       " + string(round(100*(idx/91)))+'% COMPLETE'+"                                       ")
    display("___________________________________________________________________________________________")
    loading = loading + "=";
     display(string(loading))
     display("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
end
display('                   ALL WAV FILES HAVE BEEN WRITTEN TO "OUTPUT_AUDIO" FILE');
display('                               A TOTAL OF 1365 FILES CREATED')


