
import lidario as lio

# TODO:
# Translator return multiple data structure
# Object to retrieve only metadata
# Increase raster resolution


if __name__ == '__main__':

    translator = lio.Translator("tif", "df")
    result = translator.translate("/home/becode/PycharmProjects/lidario/tests/assets/1.tif")

    print(result)
