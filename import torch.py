import torch
print(torch.cuda.is_available())  # Should print True if GPU is available
print(torch.cuda.device_count())  # Should print number of GPUs
