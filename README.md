# AZURE
# create venv and activate it
python -m venv .venv

.venv\Scripts\activate

# package installation checks
poetry init -> guides through the poetry toml file setup
poetry env info
poetry run python --version
poetry run pip list
poetry install 
poetry.lock

# downloading the model ->
1) can do it with .py file -> scripts/test_model.py
2) can do it in hugging face cli -> poetry run huggingface-cli download microsoft/phi-3-mini-4k-instruct
3) chck cache folder size for status -> C:\Users\<your_user>\.cache\huggingface\


# to check modules in the model
1) target_modules=["qkv_proj", "o_proj"] -> phi 3
2) for name, module in model.named_modules():
    print(name)


# scripts
1) datasetgenerator.py -> geenrates data (random data)
2) test_model.py -> locally downloads the model -> make sure it is downloadedable and stors in cache
3) train.py -> trains the model on local cpu using lora, takes time but this is local
4) 


# Azure VM
1) create resource grougp, attach it to vm, select proper image and gpu
2) use ssh and activate the terminal 
3) enter this in the terminal ssh -i  llm-gpu-trainer_key.pem azureuser@YOUR_PUBLIC_IP -> replace your public ip with the azure vm public ip
4) azure doesn't install nvidia gpu servers , we have to install them for ubuntu
        a) sudo apt install nvidia-utils-535         # version 535.288.01-0ubuntu0.24.04.1
            sudo apt install nvidia-utils-535-server  # version 535.288.01-0ubuntu0.24.04.2
        b) sudo reboot
        c) after reboot connect again and check nvidia-smi
        d) some times the driver wont get installed, follow microfost -> shut down, stop secure boot, restart vm -> it works like magic
6) install pacakages ion vm 
        a)python3 --version
        b)sudo apt install python3-pip python3-venv git -y
        c)python3 -m venv llm-env
            source llm-env/bin/activate
        d)pip install torch torchvision torchaudio --index-url  https://download.pytorch.org/whl/cu121
        e) tests the isatlled cuda -> python3 -c "import torch; print(torch.cuda.is_available())"
        
7) instead of doing 6 and 7 we can dockerize all the setup and reduce manual laoad
        sudo apt update
        sudo apt install docker.io -y
        sudo systemctl start docker
        sudo systemctl enable docker
8) check if nvidia container toolkit is working in docker -> 
        sudo docker run --rm --gpus all nvidia/cuda:12.1.1-runtime-ubuntu22.04 nvidia-smi

9) Misc -> to install nvidia toolkit contaner 
            a) distribution=ubuntu22.04
            b)curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
            c)curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
            d)sudo apt update
            e)sudo apt install -y nvidia-container-toolkit
            f)sudo systemctl restart docker
            g)test -> sudo docker run --rm --gpus all nvidia/cuda:12.1.1-runtime-ubuntu22.04 nvidia-smi
            h)
10) step 9 errors 
        a) sudo systemctl status docker -> permission  denied 
                sudo usermod -aG docker $USER
                exit
        b) connect back to ssh
        c) docker info | grep -i runtime
            nvidia-smi
        d) docker run --rm --gpus all nvidia/cuda:12.1.1-runtime-ubuntu22.04 nvidia-smi
11) DOcker 
        a_) pull repo in ssh from github
        b) ls -l Dockerfile
        c) bui;ld docker image -> docker build -t llm-trainer . 
        d) docker run --gpus all -it llm-trainer