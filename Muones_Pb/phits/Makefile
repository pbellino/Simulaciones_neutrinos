
INPUT=muons_phits
TARGET=track

.PHONY: clean, view

$(TARGET).out: $(INPUT)
	phits.sh $(INPUT)

clean: 
	rm -f $(TARGET).out $(TARGET).eps
	rm -f $(TARGET)_err.out $(TARGET)_err.eps
	rm -f batch.out phits.out pegs5* *-temporary.inp

view: $(TARGET).out 
	evince $(TARGET).eps &

