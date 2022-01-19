import { Component } from '@angular/core';

function log(target: any, name: any, descriptor: any) {
  console.log(target, name, descriptor)
  const origin = descriptor.value
  origin()
  return descriptor
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'pas';

}
