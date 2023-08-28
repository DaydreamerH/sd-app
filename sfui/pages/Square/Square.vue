<template>
	<view class="row">
		<uv-search v-model='con' @search="toSearch" @custom="toSearch" class='Search'></uv-search>
		<uv-tabs :list="tab_list" @change='changeTab'></uv-tabs>
		<uv-swiper :list="list" indicator indicatorMode="line" circular class='swBox' height="180" keyName="image"
			showTitle @click="swiper_Show"></uv-swiper>
		<view v-for='(imgs,index) in pairedPrevImgs' :key='index' class="ImgsBox">
			<view v-for='(img,index) in imgs' :key='img.iid'>
				<view v-if='show_time&&index==0' @click="toShow(img.iid)">
					<ImgCard v-if='show_time&&index==0' :img_url='img.source' :title='img.title'></ImgCard>
				</view>
				<view v-if='show_time&&index==1' @click="toShow(img.iid)">
					<ImgCardRight v-if='show_time&&index==1' :img_url='img.source' :title='img.title'></ImgCardRight>
				</view>
			</view>
		</view>
		<uv-load-more :status="loadAble"></uv-load-more>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				PrevList: [],
				Page: {
					page: 1,
					per_page: 4,
					tag: ""
				},
				total_pages: '',
				show_time: false,
				loadAble: "loadmore",
				list: [

				],
				tab_list: [{
					name: '总览'
				}, {
					name: '动漫卡通'
				}, {
					name: '建筑艺术',
				}, {
					name: '写实人像'
				}, {
					name: '欧美漫画'
				}],
				current: 0,
				con:''
			}
		},
		methods: {
			changeTab(item) {
				this.current = item.index
				this.Page.page = 1
				if (this.current == 0)
					this.imgSelect()
				else this.imgSelectTag()
			},
			imgSelectTag() {
				let _this = this
				let form = {}
				this.Page.tag = this.tab_list[this.current].name
				if (this.Page.page == 1) {
					this.show_time = false
					form = {
						page: this.Page.page,
						per_page: this.Page.per_page,
						tag: this.Page.tag
					}
				} else {
					form = {
						page: this.Page.page,
						per_page: this.Page.per_page,
						tag: this.Page.tag,
						iid: this.PrevList[0].iid
					}
				}
				uni.request({
					url: "http://localhost:3689/img/select_tag",
					data: form,
					method: 'POST'
				}).then(function(resp) {
					if (_this.Page.page == 1) {
						_this.PrevList = resp.data.prev_imgs
						_this.list = resp.data.hot_imgs
						_this.show_time = true
					} else _this.PrevList = _this.PrevList.concat(resp.data.prev_imgs)
					_this.total_pages = resp.data.total_pages
				})
			},
			imgSelect() {
				let _this = this
				let form = {}
				if (this.Page.page == 1) {
					this.show_time = false
					form = {
						page: this.Page.page,
						per_page: this.Page.per_page,
						tag: this.Page.tag
					}
				} else {
					form = {
						page: this.Page.page,
						per_page: this.Page.per_page,
						tag: this.Page.tag,
						iid: this.PrevList[0].iid
					}
				}
				uni.request({
					url: "http://localhost:3689/img/select",
					method: 'POST',
					data: form
				}).then(function(resp) {
					if (_this.Page.page == 1) {
						_this.PrevList = resp.data.prev_imgs
						_this.list = resp.data.hot_imgs
						_this.show_time = true
					} else _this.PrevList = _this.PrevList.concat(resp.data.prev_imgs)
					_this.total_pages = resp.data.total_pages
				})
			},
			swiper_Show(index){
				const iid = this.list[index].iid
				this.toShow(iid)
			},
			toShow(iid) {
				uni.navigateTo({
					url: '/pages/showImg/showImg?iid=' + iid
				})
			},
			toSearch(){
				uni.navigateTo({
					url:'/pages/search/search?con='+this.con
				})
			}
		},
		mounted() {
			this.imgSelect()
		},
		onReachBottom() {
			let _this = this
			this.Page.page += 1
			this.loadAble = 'loading'
			if (this.total_pages >= this.Page.page) {
				if (this.current == 0)
					this.imgSelect()
				else this.imgSelectTag()
				this.loadAble = 'loadmore'
			} else this.loadAble = 'nomore'
		},
		onPullDownRefresh() {
			let _this = this
			this.show_time = false
			this.Page.page = 1
			if (this.current == 0) this.imgSelect()
			else this.imgSelectTag()

			uni.stopPullDownRefresh()
		},
		computed: {
			isLeft(index) {
				if (index % 2 != 0) return false
				return true
			},
			pairedPrevImgs() {
				const pairedPrevImgs = [];
				for (let i = 0; i < this.PrevList.length; i += 2) {
					const pair = this.PrevList.slice(i, i + 2);
					pairedPrevImgs.push(pair);
				}
				return pairedPrevImgs;
			}
		}
	}
</script>

<style lang="scss" scoped>
	.row {
		width: 750rpx;
		height: 100vh;

		.swBox {
			width: 710rpx;
			margin-left: 20rpx;
			margin-top: 20rpx;
		}

		.ImgsBox {
			display: flex;
		}
		.Search{
			position: relative;
			top:10rpx;
		}
	}
</style>