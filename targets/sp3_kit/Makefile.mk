# Support for the Spartan 3 Starter Kit

ifneq ($(PLATFORM),sp3_kit)
	$(error "Platform should be Spartan 3 Starter Kit when using this file!?")
endif

# Settings
DEFAULT_TARGET = base
TARGET ?= $(DEFAULT_TARGET)

PROG_PORT ?= /dev/ttyUSB0
COMM_PORT ?= /dev/ttyUSB0
BAUD ?= 115200

# Image
image-flash-$(PLATFORM):
	@echo "Unsupported"
	@false

# Gateware
gateware-load-$(PLATFORM):
	$(HOME)/bin/openocd -f board/$(PLATFORM).cfg -c "init; pld load 0 $(GATEWARE_FILEBASE).bit; exit"

gateware-flash-$(PLATFORM):
	@echo "Unsupported"
	@false

# Firmware
firmware-load-$(PLATFORM):
	flterm --port=/dev/ttyUSB0 --kernel=$(FIRMWARE_FILEBASE).bin

firmware-flash-$(PLATFORM):
	@echo "Unsupported."
	@false

firmware-connect-$(PLATFORM):
	@echo "Unsupported."
	@false

firmware-clear-$(PLATFORM):
	@echo "FIXME: Unsupported?."
	@false

# Bios
bios-flash-$(PLATFORM):
	@echo "Unsupported."
	@false

# Extra commands
help-$(PLATFORM):
	@true

reset-$(PLATFORM):
	@echo "Unsupported."
	@false
