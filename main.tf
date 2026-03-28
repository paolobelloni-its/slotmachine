terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "slot" {
  name = "slot-machine:latest"
  build {
    context = "."
  }
}

resource "docker_volume" "data" {
  name = "slot_data"
}

resource "docker_container" "server" {
  name  = "slot-server"
  image = docker_image.slot.image_id

  ports {
    internal = 7777
    external = 7777
  }

  volumes {
    volume_name    = docker_volume.data.name
    container_path = "/data"
  }
}