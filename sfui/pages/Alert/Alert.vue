<template>
	<view class='row'>
		<uv-swipe-action v-if='info_list!=[]'>
			<view v-for='(info,index) in info_list' :key='index'>
				<uv-swipe-action-item :options="options" :name='info.cid + "," +index' @click='DelOrReply'>
					<CommentInfo :info='info' :index='index'></CommentInfo>
					<uv-line></uv-line>
				</uv-swipe-action-item>
			</view>
		</uv-swipe-action>
		<uv-empty mode='message' width="300" marginTop="200" 
		iconColor="#F8D9E9" iconSize='130' text='暂无消息'
		 textColor="#F8D9E9" textSize="20" v-if="info_list.length==0"></uv-empty>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				u_info: '',
				info_list: [],
				options: [{
					text: '删除',
					style: {
						backgroundColor: "#FF5A5F"
					}
				}]
			};
		},
		onShow() {
			this.u_info = uni.getStorageSync('u_info')
			let _this = this
			uni.request({
				url: 'http://8.137.96.56:3689/info/get',
				data: _this.u_info.uid,
				method: 'POST'
			}).then(function(resp) {
				_this.info_list = resp.data
			}).catch(e => {
				console.log(e)
			})
		},
		methods:{
			DelOrReply(item){
				if(item.index==0){
					const num = item.name.split(',')
					this.delInfo(num[0],num[1])
				}
			},
			delInfo(cid,index){
				const form={
					uid:this.u_info.uid,
					secret:this.u_info.secret,
					cid:cid
				}
				let _this = this
				uni.request({
					url:'http://8.137.96.56:3689/info/delete_one',
					data:form,
					method:'POST'
				}).then(function(resp){
					if(resp.data=='success'){
						_this.info_list.splice(index,1)
					}
				})
			}
		},
		computed:{
			cid_index(cid,index){
				return {
					cid:cid,
					index:index
				}
			}
		}
	}
</script>

<style lang="scss" scoped>
	.row {
		width: 750rpx;
		height: 100vh;
	}
</style>