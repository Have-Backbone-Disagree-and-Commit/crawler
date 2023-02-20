var express = require('express');
var router = express.Router();
const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const fs = require('fs');
const axios = require('axios');
const request = require('request')

let link_list = {};
let detail_data = []

async function crawl(){
  const browser = await puppeteer.launch({headless: true});
  const page = await browser.newPage();
  await page.goto('https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=-1&locations=all');

  const content = await page.content();
  const $ = cheerio.load(content);
  const lists = $("#__next > div.JobList_cn__t_THp > div > div > div.List_List_container__JnQMS > ul > li > div");
  lists.each((index, list) => {
      link_list[index] = {
          link: "https://wanted.co.kr" + $(list).find("a").attr('href')
      }
  })
  console.log(link_list)
  await browser.close();  

  function sleep(ms) {
    const wakeUpTime = Date.now() + ms;
    while (Date.now() < wakeUpTime) {}
  }

  link_length = Object.keys(link_list).length
  for(index=0; index<link_length; index++){
    console.log("[" + index + "] " + "Crawling the " + link_list[index].link + " Data...")
    detail_url = link_list[index].link
    const browser = await puppeteer.launch({headless: true});
    const page = await browser.newPage();
    await page.goto(detail_url)

    for (scroll = 0; scroll < 6000; scroll += 100){
      command = "window.scrollTo(0, " + scroll + ")"
      await page.evaluate(command); sleep(10);
    }

    const content = await page.content();
    const $ = cheerio.load(content);
    const lists = $("#__next > div.JobDetail_cn__WezJh > div.JobDetail_contentWrapper__DQDB6 > div.JobDetail_relativeWrapper__F9DT5 > div.JobContent_className___ca57");
    lists.each((index, list) => {

      // using timestamp format
      enddate = $(list).find("div.JobContent_descriptionWrapper__SM4UD > section.JobWorkPlace_className__ra6rp > div:nth-child(1) > span.body").text()
      if (enddate != "상시"){
        try{
          timestamp = new Date(enddate).getTime()
          enddate = timestamp.toString()
        }
        catch(e){
          console.log(e)
        }
      }

      detail = {
          sitename: "wanted",
          url: detail_url,
          title: "",
          collectiondate: (new Date()).getTime().toString(),
          startdate: "",
          enddate: enddate,
          companyname: $(list).find("section.JobHeader_className__HttDA > div:nth-child(2) > h6 > a").text(),
          location: $(list).find("div.JobContent_descriptionWrapper__SM4UD > section.JobWorkPlace_className__ra6rp > div:nth-child(2) > span.body").text(),
          recruitfield: "",
          recruittype: "",
          recruitclassification: "",
          personnel: "",
          salary: "",
          position: $(list).find("section.JobHeader_className__HttDA > h2").text(),
          task: $(list).find("div.JobContent_descriptionWrapper__SM4UD > section > p:nth-child(3)").text(),
          qualifications: $(list).find("div.JobContent_descriptionWrapper__SM4UD > section > p:nth-child(5)").text(),
          prefer: $(list).find("div.JobContent_descriptionWrapper__SM4UD > section.JobDescription_JobDescription__VWfcb > p:nth-child(7)").text(),
          welfare: $(list).find("div.JobContent_descriptionWrapper__SM4UD > section.JobDescription_JobDescription__VWfcb > p:nth-child(9)").text(),
          description: $(list).find("div.JobContent_descriptionWrapper__SM4UD > section.JobDescription_JobDescription__VWfcb > p:nth-child(1) > span").text(),
          stacks: $(list).find("div.JobContent_descriptionWrapper__SM4UD > section.JobDescription_JobDescription__VWfcb > p:nth-child(11)").text()
      }
      detail_data.push(detail)
    })
    console.log("Crawl Finished!\r\n")
    browser.close();
  }
  //console.log(detail_data)
  return detail_data
  

  /* saving to scv file code
  let csv = '';

  detail_data.forEach(function(row) {
    let rowData = '';
    for (let property in row) {
      let cell = row[property];
      cell = cell.toString().replace(/"/g, '""');
      rowData += `"${cell}",`;
    }
    csv += rowData.slice(0, -1) + '\n';
  });

  fs.writeFile('data.csv', csv, function(err) {
    if (err) throw err;
    console.log('File saved!');
  });*/


};

/* GET home page. */
router.get('/', async function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/crawl', async function(req, res, next) {
  await crawl().then(function(data){
    // convert data 
    const result = data.reduce((acc, curr, index) => {
      acc[index.toString()] = curr;
      return acc;
    }, {});
    console.log(result)

    url = "http://127.0.0.1:8000/elastic"
    axios.post(url, result
    ).then((res) => {
              console.log(res);
            });

  }).then(function(){
    res.sendStatus(200)
  })
});

module.exports = router;
