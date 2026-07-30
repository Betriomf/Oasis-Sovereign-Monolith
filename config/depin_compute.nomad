job "oasis-depin-node" {
  datacenters = ["macbook-laminar-01"]
  type        = "service"

  group "compute-engine" {
    count = 1

    task "powerdrop-orchestrator" {
      driver = "exec"

      config {
        command = "python3"
        args    = ["agents_core/powerdrop_stress_test.py"]
      }

      resources {
        cpu    = 500 # Limitado para evitar estrangulamiento térmico
        memory = 512 # MB
      }
    }
  }
}
