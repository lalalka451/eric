"use strict";

/**
 * Randomizes the Playwright fingerprint
 */
(() => {
  // Canvas Def
  const getImageData = CanvasRenderingContext2D.prototype.getImageData;

  const noisify = (canvas, context) => {
    const shift = {
      r: Math.floor(Math.random() * 10) - 5,
      g: Math.floor(Math.random() * 10) - 5,
      b: Math.floor(Math.random() * 10) - 5,
      a: Math.floor(Math.random() * 10) - 5,
    };
    const width = canvas.width;
    const height = canvas.height;

    if (width && height) {
      const imageData = getImageData.apply(context, [0, 0, width, height]);

      for (let i = 0; i < height; i++)
        for (let j = 0; j < width; j++) {
          const n = i * (width * 4) + j * 4;
          imageData.data[n + 0] += shift.r;
          imageData.data[n + 1] += shift.g;
          imageData.data[n + 2] += shift.b;
          imageData.data[n + 3] += shift.a;
        }

      context.putImageData(imageData, 0, 0);
    }
  };

  HTMLCanvasElement.prototype.toBlob = new Proxy(HTMLCanvasElement.prototype.toBlob, {
    apply(target, self, args) {
      noisify(self, self.getContext("2d"));
      return Reflect.apply(target, self, args);
    },
  });

  HTMLCanvasElement.prototype.toDataURL = new Proxy(HTMLCanvasElement.prototype.toDataURL, {
    apply(target, self, args) {
      noisify(self, self.getContext("2d"));
      return Reflect.apply(target, self, args);
    },
  });

  CanvasRenderingContext2D.prototype.getImageData = new Proxy(CanvasRenderingContext2D.prototype.getImageData, {
    apply(target, self, args) {
      noisify(self.canvas, self);
      return Reflect.apply(target, self, args);
    },
  });

  // WebGL Def
  // ... (Include the rest of your WebGL and other protection code here)

  // Font Def
  Object.defineProperty(HTMLElement.prototype, "offsetHeight", {
    get: new Proxy(Object.getOwnPropertyDescriptor(HTMLElement.prototype, "offsetHeight").get, {
      apply(target, self, args) {
        try {
          const height = Math.floor(self.getBoundingClientRect().height);
          const noise = Math.floor(Math.random() * 2) === 0 ? -1 : 1;
          return height + noise;
        } catch (e) {
          return Reflect.apply(target, self, args);
        }
      },
    }),
  });

  Object.defineProperty(HTMLElement.prototype, "offsetWidth", {
    get: new Proxy(Object.getOwnPropertyDescriptor(HTMLElement.prototype, "offsetWidth").get, {
      apply(target, self, args) {
        const width = Math.floor(self.getBoundingClientRect().width);
        const noise = Math.floor(Math.random() * 2) === 0 ? -1 : 1;
        return width + noise;
      },
    }),
  });

  // Audio Def
  const context = {
    BUFFER: null,
    getChannelData: function (e) {
      e.prototype.getChannelData = new Proxy(e.prototype.getChannelData, {
        apply(target, self, args) {
          const results_1 = Reflect.apply(target, self, args);

          if (context.BUFFER !== results_1) {
            context.BUFFER = results_1;

            for (let i = 0; i < results_1.length; i += 100) {
              const index = Math.floor(Math.random() * i);
              results_1[index] += Math.random() * 0.0000001;
            }
          }

          return results_1;
        },
      });
    },
    createAnalyser: function (e) {
      e.prototype.__proto__.createAnalyser = new Proxy(e.prototype.__proto__.createAnalyser, {
        apply(target, self, args) {
          const analyser = Reflect.apply(target, self, args);

          analyser.__proto__.getFloatFrequencyData = new Proxy(analyser.__proto__.getFloatFrequencyData, {
            apply(target, self, args) {
              Reflect.apply(target, self, args);
              for (let i = 0; i < args[0].length; i += 100) {
                args[0][i] += Math.random() * 0.1;
              }
              return;
            },
          });

          return analyser;
        },
      });
    },
  };

  context.getChannelData(AudioBuffer);
  context.createAnalyser(AudioContext);
  context.createAnalyser(OfflineAudioContext);

  // Disable WebRTC if needed
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia = undefined;
  }

  // Remove webdriver property
  Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
  });
})();