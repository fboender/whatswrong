ZIP_SRCDIR=src/
ZIP_TARGET=whatswrong.zip
zip: clean
	cd $(ZIP_SRCDIR) && \
	  zip -r $(ZIP_TARGET) * && \
	  mv $(ZIP_TARGET) ..

clean:
	find ./ -name "*.pyc" -delete
	rm -f $(ZIP_TARGET)
