// vim: https://github.com/leafgarland/typescript-vim/tree/master/syntax
import {HTMLBox, HTMLBoxView} from "models/layouts/html_box"
import {Slider} from "models/widgets/slider"
import {div} from "core/dom"
import * as p from "core/properties"

export class CustomView extends HTMLBoxView {
  model: Custom

  private content_el: HTMLElement

  connect_signals(): void {
    super.connect_signals()
    this.connect(this.model.slider.change, () => this._update_text())
  }

  render(): void {
    // BokehJS Views create <div> elements by default, accessible as ``this.el``.
    // Many Bokeh views extend this default <div> with additional elements
    // (e.g. <canvas>), and instead do things like paint on the HTML canvas.
    // In this case though, we change the contents of the <div>, based on the
    // current slider value.
    super.render()

    this.content_el = div({style: {
      textAlign: "center",
      fontSize: "1.0em",
      fontWeigth: "bold",
      padding: "2px",
      color: "#000000",
      backgroundColor: "#ffffff",
    }})
    this.el.appendChild(this.content_el)

    this._update_text()
  }

  private _update_text(): void {
    var days  = ('0' + parseInt(String(parseInt(`${this.model.slider.value}`) / 24))).slice(-2);
    var hours = ('0' + parseInt(`${this.model.slider.value}`) % 24).slice(-2);
    //var mins  = ('0' + parseInt(String((parseFloat(`${this.model.slider.value}`) * 60) % 59.99))).slice(-2);
    this.content_el.textContent = `${days}d ${hours}h`
  }
}

export namespace Custom {
  export type Attrs = p.AttrsOf<Props>

  export type Props = HTMLBox.Props & {
    slider: p.Property<Slider>
  }
}

export interface Custom extends Custom.Attrs {}

export class Custom extends HTMLBox {
  properties: Custom.Props

  constructor(attrs?: Partial<Custom.Attrs>) {
    super(attrs)
  }

  static initClass(): void {
    // The ``type`` class attribute should generally match exactly the name
    // of the corresponding Python class.
    this.prototype.type = "Custom"

    // If there is an associated view, this is typically boilerplate.
    this.prototype.default_view = CustomView

    // The define block adds corresponding "properties" to the JS model. These
    // should normally line up 1-1 with the Python model class. Most property
    // types have counterparts, e.g. bokeh.core.properties.String will be
    // ``p.String`` in the JS implementation. Any time the JS type system is not
    // yet as complete, you can use ``p.Any`` as a "wildcard" property type.
    this.define<Custom.Props>({
      slider: [ p.Any    ],
    })

    this.override({
      margin: 5,
    })
  }
}
Custom.initClass()
