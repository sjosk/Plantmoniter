   AFRAME.registerComponent("controller", {
    schema: {
      connect: { type: "selector" },
      disconnect: { type: "selector" },
    },
  
    init: function () {
        let client
    

      this.data.connect.addEventListener("click", (event) => {
        console.log(event.target.getAttribute("material").color);
        this.data.connect.setAttribute("material", { emissiveIntensity: "0.8" });
        this.data.disconnect.setAttribute("material", {
          emissiveIntensity: "0.1",
        });
        //Create a new client with ID of the marker
        client = mqtt.connect("ws://mqtt.cetools.org:8080");
        client.on("connect", () => {
        console.log("Connected");
        this.startMqtt(client); //if connected, subscribe to the topics
        });
        client.on("error", (error) => {
        console.log(error);
        });
        
      });
      this.data.disconnect.addEventListener("click", (event) => {
        console.log(event.target.getAttribute("material").color);
        this.data.connect.setAttribute("material", { emissiveIntensity: "0.1" });
        this.data.disconnect.setAttribute("material", {
          emissiveIntensity: "0.8",
        });
      });
    },

    //Custom components and MQTT
    startMqtt: function (client) {
        client.subscribe('student/CASA0014/plant/ucfnswu/moisture');
        client.subscribe('student/CASA0014/plant/ucfnswu/temperature');
        client.subscribe('student/CASA0014/plant/ucfnswu/humidity')
      
        client.on('message', (topic, message) => {
          //Called each time a message is received
          console.log('Received message:', topic, message.toString());
      
          if (topic.includes('moisture')) {
              document.querySelector('#moisture').setAttribute('value', 'Moisture: ' + parseFloat(message.toString()).toFixed(2).toString() + '%');
          }
      
          if (topic.includes('temperature')) { //temperature
              document.querySelector('#temperature').setAttribute('value', 'Temperature: ' + parseFloat(message.toString()).toFixed(2).toString() + '°C');
          }
      
          if (topic.includes('humidity')) { //humidity
              document.querySelector('#humidity').setAttribute('value', 'Humidity: ' + parseFloat(message.toString()).toFixed(2).toString() + '%');
          }
          
          if (topic.includes("moisture")) {
            document
              .querySelector("#moisture")
              .setAttribute(
                "value",
                "Moisture: " + parseFloat(message.toString()).toFixed(2).toString() + "%"
              );
            this.colourLeaf(message);
          }
        })
      },
      
      stopMqtt: function (client) {
          client.end(true);
          console.log('connection closed');
      },

      colourLeaf: function (msg) {
        const colorScaleFunction = d3
          .scaleThreshold()
          .domain([0, 40])
          .range([
            [105 / 255, 179 / 255, 76 / 255], //0-13
            [250 / 255, 183 / 255, 51 / 255], //14-26
            [255 / 255, 13 / 255, 13 / 255], //26-40
          ]);
      
        let modelEl = document.querySelector("#_plant");
        console.log(modelEl.object3D.children);
      
        let leaf = modelEl.object3D.children[0].children.find(
          (el) => el.name == "leaf003"
        );
        leaf.material.color.fromArray(colorScaleFunction(parseInt(msg)));
      },

  });