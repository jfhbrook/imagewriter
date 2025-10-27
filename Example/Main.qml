import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
  width: 300
  height: 200
  visible: true
  title: "Hello World!"

  readonly property list<string> texts: ["hey", "there", "sup", "dawg"]

  function setText() {
    var i = Math.round(Math.random() * 3)
    text.text = texts[i]
  }

  ColumnLayout {
    anchors.fill: parent

    Text {
      id: text
      text: "Hello World"
      Layout.alignment: Qt.AlignCenter
    }

    Button {
      text: "Click me"
      Layout.alignment: Qt.AlignCenter
      onClicked: setText()
    }
  }
}
