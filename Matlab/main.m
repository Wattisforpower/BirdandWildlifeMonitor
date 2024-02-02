%%
BarnSwallowData = AudioBarnswallowMBSplitDataBarnSwallow1_split_1wav.';

%%

Data_mean = mean(BarnSwallowData);
Data_Max = max(BarnSwallowData);
Data_Min = min(BarnSwallowData);

NormalizedData = (BarnSwallowData - Data_mean) / (Data_Max - Data_Min);

%%

Data_std = std(BarnSwallowData);

StandardizedData = (BarnSwallowData - Data_mean) / (Data_std);

%%
figure
subplot(3, 1, 1);
histogram(BarnSwallowData);
title('Before Normalization or Standardization');
subplot(3, 1, 2);
histogram(NormalizedData);
title('After Normalization');
subplot(3, 1, 3);
histogram(StandardizedData);
title('After Standardization')