import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Console } from 'console';
import {ApiService} from '../api.service';
import { IdVideo } from '../video.interface';
import { wordErrorRate } from "word-error-rate";
import { waitForAsync } from '@angular/core/testing';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  videos : Array<IdVideo> = [{id:0,name:"Select a video",url:"null"},
  {id:1, name :"Liverpool Kits",url:"FNHuPeacJ9c"},
  {id:2, name:"Pochettino tactics",url:"elaTzZT3QyY"},
  {id:3, name:"Adele - Hello", url:"be12BC5pQLE"},
  {id:4, name:"Jack Ma Motivational",url:"X9JExlvPwcs"}]
  
    clickCounter: number = 3;
  totalAngularPackages: any;

  test : string="GROS TEST";
  data : any;

  googleScript :any;

  werIbm : any;
  werAws : any;

  leviIbm : any;
  leviAws : any;

  ibmScript : any='faire';
  ibmEnd : boolean = false;

  amazonScript : any="Faire";
  amazonEnd : boolean = false;  

  selectedVideo : number=0;
  urlVideo : string="";
  endTask : boolean=false;

  constructor(private api:ApiService) {  }

  ngOnInit() { }


  
  get_ibm(){
    this.api.getDataIbm(this.selectedVideo).subscribe(data=>{
      this.data = data;
      this.ibmScript = this.data.result;
      this.ibmEnd = true;
      
      // this.checkTaskEnd();
    })
  }

  get_amazon(){
    this.api.getDataAmazon(this.selectedVideo).subscribe(data=>{
      this.data = data;
      this.amazonScript = this.data.result;
      this.amazonEnd = true;
      // this.checkTaskEnd();
    })
  }

  get_google(){
    this.api.getDataGoogle(this.selectedVideo).subscribe(data=>{
      this.data = data;
      this.googleScript = this.data.result;
      // this.checkTaskEnd();
    })
  }

  checkTaskEnd(){
    
    this.endTask = true;

  }

  

  levenshteinDistance(str1:string, str2:string) {
    const track = Array(str2.length + 1).fill(null).map(() =>
    Array(str1.length + 1).fill(null));
    for (let i = 0; i <= str1.length; i += 1) {
       track[0][i] = i;
    }
    for (let j = 0; j <= str2.length; j += 1) {
       track[j][0] = j;
    }
    for (let j = 1; j <= str2.length; j += 1) {
       for (let i = 1; i <= str1.length; i += 1) {
          const indicator = str1[i - 1] === str2[j - 1] ? 0 : 1;
          track[j][i] = Math.min(
             track[j][i - 1] + 1, // deletion
             track[j - 1][i] + 1, // insertion
             track[j - 1][i - 1] + indicator, // substitution
          );
       }
    }
    return track[str2.length][str1.length];
 };

  selectChangeHandler (event: any) {
    
    this.selectedVideo = event.target.value;
    var index = Number(this.selectedVideo);
    this.urlVideo = this.videos[index].url;
  }

  updatelevi(){

    this.leviIbm =  this.levenshteinDistance(this.ibmScript,this.amazonScript);
    this.leviAws =  this.levenshteinDistance(this.ibmScript,this.amazonScript)

  }

  updatewer(){

    this.werAws = wordErrorRate(this.amazonScript, this.googleScript)
    this.werAws = 1 - Number((this.werAws).toFixed(2));
    this.werIbm = wordErrorRate(this.ibmScript,this.googleScript)
    this.werIbm = 1 - Number((this.werIbm).toFixed(2));
  }


}
