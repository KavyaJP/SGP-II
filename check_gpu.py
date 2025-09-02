import torch


def check_gpu():
    """
    Checks if PyTorch can access the GPU and prints the status.
    """
    print("--- Checking for GPU Acceleration ---")

    # The main check: torch.cuda.is_available() returns True if a GPU is found
    is_available = torch.cuda.is_available()

    if is_available:
        print("\n✅ Success! GPU acceleration is available.")
        # Get the number of available GPUs
        gpu_count = torch.cuda.device_count()
        print(f"Number of GPUs found: {gpu_count}")

        # Print details for each GPU
        for i in range(gpu_count):
            gpu_name = torch.cuda.get_device_name(i)
            print(f"  - GPU {i}: {gpu_name}")
    else:
        print("\n❌ Failed. GPU acceleration is not available.")
        print("PyTorch will use the CPU instead. This will be very slow.")
        print("Please ensure you have installed the correct NVIDIA drivers.")


if __name__ == "__main__":
    check_gpu()
