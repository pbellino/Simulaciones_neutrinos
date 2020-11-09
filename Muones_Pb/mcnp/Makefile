
INPUT=muons_mcnp
TARGET=out

.PHONY: clean, view

$(TARGET).o: $(INPUT)
	mcnp6 tasks 8 i=$(INPUT) n=out.

clean: 
	rm -f $(TARGET).o $(TARGET).r

view: $(TARGET).o 
	grep "No creation" $(TARGET).o

