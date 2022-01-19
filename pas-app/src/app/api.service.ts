import { Injectable } from '@angular/core';
import { HttpClient,HttpHeaders } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http:HttpClient) { }

  getDataIbm(id:number){

    let url = 'http://localhost:5000/ibm?id=' + id.toString();
    return this.http.get(url);
  }

  getDataAmazon(id:number){

    let url = 'http://localhost:5000/amazon?id=' + id.toString();
  return this.http.get(url);
  }
  
  getDataGoogle(id:number){

    let url = 'http://localhost:5000/google?id=' + id.toString();
  return this.http.get(url);
  }  
}
