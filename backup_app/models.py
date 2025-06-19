from django.db import models

class Machine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class BackupFolder(models.Model):
    machine = models.ForeignKey(Machine, related_name='backup_folders', on_delete=models.CASCADE)
    path = models.CharField(max_length=255)  # caminho da pasta no disco C da máquina
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.machine.name} - {self.path}"
