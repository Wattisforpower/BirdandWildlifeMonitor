clear all
close all
clc

DEF_PLOT = 1;
DEF_OUT = 1;




        [signal, Fs] = audioread('49_5.wav');
        signal = transpose(signal(:,1));
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %PLOT WAV FILE
        if(DEF_PLOT == 1)
            figure(1)
            subplot(311)
            hold on;
            title('Input Signal');
            t1 = 0:1/Fs:(length(signal)-1)/Fs;
            xlabel("Time [S]");
            ylabel("Amplitude [Au]");
            plot(t1,signal,'b');
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %SPECTRAL ENERGY CALCULATION
        SAMPLES_PER_FRAME = 1000;
        ste = sum(buffer(signal.^2, SAMPLES_PER_FRAME));
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %PLOT STE
        if(DEF_PLOT == 1)
            subplot(312)
            hold on;
            xlabel("Time [S]");
            ylabel("Amplitude [Au]");
            t = 0:(SAMPLES_PER_FRAME*10/length(signal)):(length(signal)-1)/Fs;
            plot(t,ste,'b');
            title("Short Time Energy Analysis")
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %CALCULATING AVG THRESHOLD
        ste_avg_len = 50;
        ste_avg_array = ones(1,ste_avg_len);
        ste_calculated_avg = zeros(1,length(ste));
        activity = zeros(1,length(ste));
        expanded_activity = zeros(1,length(signal));
        sum = 0;
        ste_idx = 1;
        THRESHOLD = 0.1;
        ste_frame_count = 0;
        ste_frame_count_BASE = 5;
        for idx = 1: length(ste)
            if(idx == 1)
                ste_avg_array = ones(1,ste_avg_len) *ste(idx) ;
            else
                ste_avg_array(ste_idx) = ste(idx);
            end
        
            ste_idx = ste_idx + 1;
            if(ste_idx > ste_avg_len)
                ste_idx = 1;
            end
            sum = 0;
            for n = 1: length(ste_avg_array)
                sum = sum + ste_avg_array(n);
            end
            ste_calculated_avg(idx) = sum/ste_avg_len;
            % if(idx == 1)
            % 
            %     for n = 1:length(ste_avg_array)
            %         ste_avg_array(n) = ste(idx)
            %     end
            % end
        
            if(ste_calculated_avg(idx) + (ste_calculated_avg(idx)*THRESHOLD)<=ste(idx))
                activity(idx) = 1;
                ste_frame_count = ste_frame_count_BASE;
            elseif (ste_frame_count > 0)
                activity(idx) = 1;
                ste_frame_count = ste_frame_count - 1;
            else
                activity(idx) = 0;
            end
        end
        if(DEF_PLOT == 1)
            plot(t,ste_calculated_avg,'r');
            legend("Short Time Energy","Adaptive Threshold");
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %PLOT NOISE VS SIGNAL 
        scaling_factor =  length(signal) / length(activity) ;
        
        for idx = 0:length(activity)-1
            lower = (idx * scaling_factor) + 1;
            upper = lower + scaling_factor;
            if upper > length(signal)
                upper = length(signal);
            end
        
            if (activity(idx+1) == 1)
                
                expanded_activity(lower:upper) = 1;
            else
                expanded_activity(lower:upper) = 0;
            end
        end
        
        separated_signal = zeros(1,length(signal));
        separated_noise = zeros(1,length(signal));
        
        for idx = 1:length(signal)
            if(expanded_activity(idx) == 1)
                separated_signal(idx) = signal(idx);
                separated_noise(idx) = NaN;    
            else
                separated_signal(idx) = NaN;
                separated_noise(idx) = signal(idx); 
            end
        end
        if(DEF_PLOT == 1)
            subplot(313)
            hold on
            t1 = 0:1/Fs:(length(signal)-1)/Fs;
            plot(t1,separated_signal,'Color' , '#0072BD' )
            plot(t1,separated_noise,'Color' , '#D95319' )
            xlabel("Time [S]");
            ylabel("Amplitude [Au]");
            title('Noise Detection');
            legend('Detected Bird','Detected Noise');
            hold off
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %FFT OF FRAMES
        noise_avg_array_length = 2;
        noise_array_head = 1;
        max_mag_lim = 0;
        
        for idx = 0:length(activity)-1
            lower = (idx * scaling_factor) + 1;
            upper = lower + scaling_factor;
            if upper > length(signal)
                upper = length(signal);
            end
            frame_fft = fft(signal(lower:upper));
        
            L = length(signal(lower:upper));
            P2 = abs(frame_fft/L);
            P1 = P2(1:round(L/2)+1); %fft y values  
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %PLOT FFT 
            f = Fs/L*(0:(L/2)+1);  
            max_test = max(P1);
            if(max_test > max_mag_lim)
                max_mag_lim = (max_test * 1.1);
            end
        
            if(DEF_PLOT == 1)
                % figure(2)
                % plot(f(1:length(P1)),P1,"LineWidth",3)
                % hold on
                % title("Frequency Spectrum")
                % ylim([0 max_mag_lim])
                % xlabel("Frequency [Hz]");
                % ylabel("Magnitue [Au]");
            end
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            if(idx == 0)
                noise_avg_array = zeros(noise_avg_array_length,length(P1));
                noise_avg = zeros(1,length(P1));
                output_ffts = zeros(length(activity),length(P1));
                
                actual_noise_avg_array = zeros(noise_avg_array_length,length(P1));
                actual_noise_avg = zeros(1,length(frame_fft));
                actual_output_ffts = zeros(length(activity),length(frame_fft));
            end
        
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %NOISE AVERAGING
            if (activity(idx+1) == 0)%frame was detected as noise
             
                %add to rolling buffer
                noise_avg_array(noise_array_head,1:length(P1)) = P1;
                noise_array_head = noise_array_head + 1;
                if(noise_array_head > noise_avg_array_length)
                    noise_array_head = 1;
                end
                
                %get avg values
                noise_avg = 0;
                for m=1:noise_avg_array_length
                    noise_avg = noise_avg + noise_avg_array(m,:);
                end
                noise_avg = noise_avg/(noise_avg_array_length);     
            end
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            if (activity(idx+1) == 0)%frame was detected as noise
             
                %add to rolling buffer
                actual_noise_avg_array(noise_array_head,1:length(frame_fft)) = frame_fft;
                noise_array_head = noise_array_head + 1;
                if(noise_array_head > noise_avg_array_length)
                    noise_array_head = 1;
                end
                
                %get avg values
                actual_noise_avg = 0;
                for m=1:noise_avg_array_length
                    actual_noise_avg = actual_noise_avg + actual_noise_avg_array(m,:);
                end
                actual_noise_avg = actual_noise_avg/noise_avg_array_length;     
            end
        
            if(DEF_PLOT == 1)
                % plot(f(1:length(noise_avg)),noise_avg,"LineWidth",3)
                % legend('Signal Frequency','Estimated Noise')
                % pause(0.0001)
                % hold off
            end
        
        
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            zero_pad = zeros(1,length(actual_noise_avg)-length(frame_fft));
            actual_output_ffts((idx+1),:) = [frame_fft zero_pad] - actual_noise_avg;
            
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %INVERSE FFT
        [rows, cols]=size(actual_output_ffts);
        
        output_signal = [];
        for idx = 1:rows
            test = ifft(actual_output_ffts(idx,:));
            output_signal = [output_signal test];
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %PLOT OUTPUT
        output_signal = real(output_signal);
        if(DEF_PLOT == 1)
            figure(3)
            hold on
            plot(1:length(signal),signal)
            plot(1:length(output_signal),output_signal)
            legend("signal","output")
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %GET ACCURACY
        [referenceSignal, Fs] = audioread('49_55.wav');
        referenceSignal = transpose(referenceSignal(:,1));
        testSignal = output_signal(1:length(referenceSignal));
        input_testSignal = signal(1:length(referenceSignal));
        
        env_val = 500;
        [ref_up,ref_lo] = envelope(referenceSignal,env_val,'rms');
        [test_up,test_lo] = envelope(testSignal,env_val,'rms');
        [in_test_up,in_test_lo] = envelope(input_testSignal,env_val,'rms');
        
        accuracy = 100*(dot( test_up, ref_up ) / ( norm(test_up) * norm(ref_up) ));
        accuracy2 = 100*(dot( in_test_up, ref_up ) / ( norm(in_test_up) * norm(ref_up) ));
        improvement = abs(accuracy - accuracy2);

        audiowrite( 'output.wav' , output_signal , Fs ) 
       output_signal;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PLOT TEST RESULTS
figure(4)
hold on
subplot(311)
t1 = 0:1/Fs:(length(input_testSignal)-1)/Fs;
plot(t1,input_testSignal)
title("Input Audio");
xlabel("Time [S]")
ylabel("Amplitude [Au]")

subplot(312)
t1 = 0:1/Fs:(length(testSignal)-1)/Fs;
plot(t1,testSignal)
title("Noise Reduced Audio");
xlabel("Time [S]")
ylabel("Amplitude [Au]")

subplot(313)
t1 = 0:1/Fs:(length(referenceSignal)-1)/Fs;
plot(t1,referenceSignal)
title("Clean Audio");
xlabel("Time [S]")
ylabel("Amplitude [Au]")


